## UK National Rail Performance 2024 - Capstone Project

**Contributors:** Brian Levesque, Ilackkeya Bhavananthi, Osman Nayeem

**Instructor:** James-Lee Meredith

**Teaching assistant**: Dylan Gleason 

**Program Manager**: William Westley

**Institution:** Grand Circus

### Description

Welcome to our Repository! This repository hosts our Grand Circus's Final Capstone Project on Data Analytics and Engineering. The project has extensive data engineering and data analytics workflows which is essentially built to analyze the UK National Rail Schedule Performance. Our Client, UK National Railway Board of Directors wanted to understand the UK National Schedule Performance, delay compensation efficiency of Train Operating Companies (TOCs) in enhancing user experience and build a predictive model to predict any delay of a scheduled train.

As Data Analysts, we gathered essential data from [UK National Rail Data Portal](https://opendata.nationalrail.co.uk/) accessing API’s Darwin feed and additional data from [ORR](https://dataportal.orr.gov.uk/) and [Network Rail](https://www.networkrail.co.uk/) to do our analysis. We developed a scalable data pipeline architecture using Kafka and Docker, hosted the live-streaming data (after necessary transformation steps) in AWS-RDS PostgreSQL database and performed comprehensive data ingestion, pre-processing and analysis to interpret the key insights.

### Dependencies

1. Data Pipeline tools: Docker, Apache Kafka, Apache Spark
2. Database: AWS-RDS & PostgreSQL
3. Python: sqlalchemy, psycopg2, json, glob, xml.etree.ElementTree, logging, time, pandas, Numpy, datetime, matplotlib, seaborn, warnings, OSGB36toWGS84 from bng_latlon, sklearn
4. PowerBI

### Workflow

#### 1. **Setting up Data Pipeline**

Docker images for the following applications have been built and docker container was composed to start the pipeline each of which performs the following functions:

**Kafka Zookeeper**: A service necessary for running the Kafka broker. It helps in maintaining the configuration information and provides distributed synchronization.

**Kafka Broker**: The heart of the Kafka system that maintains the published data. Each Kafka broker can handle terabytes of messages without performance impact.

**Kafka Producer (Python)**: This application pulls data from the National Rail APIs and publishes it to Kafka. It's designed to run indefinitely, continually pulling and publishing data.

**Kafka Consumer (Spark)**: A Spark application that consumes data from Kafka, processes it and writes the result to a PostgreSQL database.

**PostgreSQL Database (db)**: Stores the processed data from the Spark consumer for later analysis.

#### 2. **Ingesting Data and Pre-processing**

Retrieved data from PostgreSQL database and performed necessary Data Ingestion and Pre-processing and the cleaned data was exported into csv for further data visualizations in PowerBI ([UK National Rail Data_Analysis_Final.ipynb](https://github.com/BrianLevesque/GC_CapstoneProject/blob/feature-ilackkeya/UK%20National%20Rail%20Data_Analysis_Final.ipynb)).

#### 3. **Predictive Analytics**

Built a predictive analytics model on predicting the delay using Logistic Regression model yielding an accuracy of 91.25%.  

#### 4. **Data Visualizations**

Gathered visual insights utilizing matplotlib, seaborn libraries and Power BI ([UK National Rail Performance Overview.pbix](https://github.com/BrianLevesque/GC_CapstoneProject/blob/feature-ilackkeya/UK%20National%20Rail%20Performance%20Overview.pbix)) to answer our questions. 

### For more information

Please review the directed links or [pdf](https://github.com/BrianLevesque/GC_CapstoneProject/blob/feature-ilackkeya/UK%20National%20Rail%20Data_Analysis_Final.pdf) or [PPTX](https://github.com/BrianLevesque/GC_CapstoneProject/blob/feature-ilackkeya/UK%20National%20Rail%20Performance%202024.pptx) files.

If you have any questions or feedback, please feel free to reach out to any of the authors.

- Brian Levesque brian.lev722@gmail.com

- Ilackkeya Bhavananthi bsilackkeya21@gmail.com

- Osman Nayeem osman_nayeem@yahoo.com 


