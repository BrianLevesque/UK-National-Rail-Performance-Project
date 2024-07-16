import os
import pandas as pd
import glob
import json
import datetime as dt
import xml.etree.ElementTree as ET
import logging
import time
from sqlalchemy import create_engine

# Set up logging
logging.basicConfig(filename='etl.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

PARQUET_DIRECTORY = './xml/'

DATABASE_URL = os.getenv("DATABASE_URL")
TABLE_NAME = 'darwin'  
PARQUET_FILE_THRESHOLD = 10
POLLING_INTERVAL_SECONDS = 60 

def parse_xml(xml_content):
    logging.info('Starting to parse XML content.')
    try:
        root = ET.fromstring(xml_content)

        results = []
        for ur in root.findall('{http://www.thalesgroup.com/rtti/PushPort/v16}uR'):
            for ts in ur.findall('{http://www.thalesgroup.com/rtti/PushPort/v16}TS'):
                result = {
                    'rid': ts.attrib.get('rid'),
                    'uid': ts.attrib.get('uid'),
                    'ssd': ts.attrib.get('ssd'),
                    'updateOrigin': ur.attrib.get('updateOrigin'),
                }
                locations = []
                for location in ts.findall('{http://www.thalesgroup.com/rtti/PushPort/Forecasts/v3}Location'):
                    location_data = {
                        'tpl': location.attrib.get('tpl'),
                        'wtp': location.attrib.get('wtp'),
                        'wta': location.attrib.get('wta'),
                        'wtd': location.attrib.get('wtd'),
                        'pta': location.attrib.get('pta'),
                        'ptd': location.attrib.get('ptd'),
                    }
                    # note: might want to add 'pass' here and around 112 below. it might occasionally appear
                    # along with/instead of arr/dep.
                    for tag in ['arr', 'dep', 'plat', 'length']:
                        tag_element = location.find("{http://www.thalesgroup.com/rtti/PushPort/Forecasts/v3}" + tag)
                        if tag_element is not None:
                            location_data[tag] = tag_element.text or tag_element.attrib
                    locations.append(location_data)
                result['locations'] = locations
                results.append(result)
        logging.info('Finished parsing XML content.')
        return results
    except Exception as e:
        logging.exception(f"Error occurred while parsing XML data: {e}")

def parse_parquet_directory(dir_path):
    logging.info(f'Starting to parse Parquet files in directory {dir_path}.')
    try:
        # Find all parquet files in the directory
        parquet_files = glob.glob(f'{dir_path}/*.parquet')
        logging.info('Found %s parquet files.', len(parquet_files))

        all_data = []
        for file_path in parquet_files:
            logging.info('Parsing file: %s', file_path)
            df = pd.read_parquet(file_path)

            # Iterate over the 'value' column and parse the XML content
            for xml_content in df['value']:
                xml_content = xml_content.replace('\\"', '"').strip('"')
                parsed_data = parse_xml(xml_content)
                all_data.extend(parsed_data)

        # Convert the list of dictionaries to a dataframe
        all_data_df = pd.DataFrame(all_data)
        logging.info(f'Finished parsing Parquet files in directory {dir_path}.')
        return all_data_df
    except Exception as e:
        logging.exception(f"Error occurred while parsing parquet directory: {e}")

def add_seconds(t):
    if t is not None and isinstance(t, str):
        if len(t) == 5:  # length of "HH:MM" is 5
            return t + ':00'  # append ":00"
        else:
            return t

def transform(df):
    logging.info('Starting to transform data.')
    try:
        # explode the list column into separate rows
        exploded_df = df.explode('locations')

        # create separate columns from dictionary keys
        final_df = exploded_df['locations'].apply(pd.Series)

        # merge with the original df
        final_df = pd.concat([exploded_df.drop('locations', axis=1), final_df], axis=1)

        # reset the index of final_df
        final_df = final_df.reset_index()

        # Convert time columns to datetime.time
        time_cols = ['wtp', 'wta', 'wtd']
        for col in time_cols:
            final_df[col] = final_df[col].apply(add_seconds)
            final_df[col] = pd.to_datetime(final_df['ssd'] + ' ' + final_df[col], format='%Y-%m-%d %H:%M:%S')

        final_df = final_df.loc[final_df['arr'].notnull() & final_df['dep'].notnull()]

        final_df['aat'] = final_df['arr'].apply(lambda d: d.get('et'))
        final_df['adt'] = final_df['dep'].apply(lambda d: d.get('et')) 

        final_df['a_delay'] = final_df['arr'].apply(lambda d: d.get('delayed'))
        final_df['d_delay'] = final_df['dep'].apply(lambda d: d.get('delayed'))

        # Convert 'delayed' to boolean
        final_df['a_delay'] = final_df['a_delay'].map({'true': True, None: False})
        final_df['d_delay'] = final_df['d_delay'].map({'true': True, None: False})

        time_cols = ['pta', 'ptd', 'aat', 'adt']
        for col in time_cols:
            final_df[col] = pd.to_datetime(final_df['ssd'] + ' ' + final_df[col], format='%Y-%m-%d %H:%M')
        
        logging.info('Finished transforming data.')
        # Now, you can drop the original 'index' column if you want
        return final_df.drop(columns=['index', 'arr', 'dep'])\
                       .rename(columns={
                                'rid': 'route_id',
                                'uid': 'unique_id',
                                'ssd': 'service_start_date',
                                'updateOrigin': 'update_origin',
                                'tpl': 'train_platform',
                                'wtp': 'working_time_pass',
                                'wta': 'working_time_arrival',
                                'wtd': 'working_time_departure',
                                'pta': 'planned_time_arrival',
                                'ptd': 'planned_time_departure',
                                'aat': 'actual_arrival_time',
                                'adt': 'actual_departure_time',
                                'plat': 'platform',
                                'length': 'train_length',
                                'et': 'estimated_time',
                                'src': 'source',
                                'at': 'actual_time',
                                'atClass': 'actual_time_class',
                                'a_delay': 'is_delayed_arrival',
                                'd_delay': 'is_delayed_departure',
                                'srcInst': 'source_instance',
                                'etmin': 'estimated_time_minutes'
                            })
    except Exception as e:
        logging.exception(f"Error occurred while transforming data: {e}")


def write_to_postgres(df, db_url, table_name):
    engine = create_engine(db_url)
    df.to_sql(table_name, engine, if_exists='append', index=False)

def get_parquet_files(dir_path):
    # Find all parquet files in the directory
    return glob.glob(f'{dir_path}/*.parquet')

def main():
    while True:  # Run indefinitely
        try:
            parquet_files = get_parquet_files(PARQUET_DIRECTORY)

            if len(parquet_files) >= PARQUET_FILE_THRESHOLD:
                logging.info(f'Found {len(parquet_files)} new Parquet files.')
                df = parse_parquet_directory(PARQUET_DIRECTORY)
                df = transform(df)
                if 0 in df.columns:
                    df = df.drop([0], axis=1)

                formatted_date = dt.datetime.now().strftime('%Y%m%d%H%M%S')
                df.to_parquet(f'data/rail_data_cleaned_{formatted_date}.parquet', index=None)
                df.to_csv(f'data/rail_data_cleaned_{formatted_date}.csv', index=None)

                write_to_postgres(df, DATABASE_URL, TABLE_NAME)  # write to Postgres

                logging.info('Successfully wrote to output files and Postgres.')

                # Delete or move the processed files to prevent them from being processed again
                for file_path in parquet_files:
                    os.remove(file_path)

        except Exception as e:
            logging.exception("Error occurred in the main function:")

        # Sleep for the polling interval before checking again
        time.sleep(POLLING_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()