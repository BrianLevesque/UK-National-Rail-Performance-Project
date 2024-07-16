## UK National Rail Data Analysis
A Data Analysis looking into the UK National Rail system.
### Description
This data analysis takes in data from the UK National Rail API’s Darwin feed (https://opendata.nationalrail.co.uk/) and a few other sources. Loaded it in a PostgreSQL database. It cleans the data before performing analysis using pandas and PowerBI to answer the following questions: Where and How to get the data? What is in our data? What are we going to answer? Are the trains delayed? How long are the trains delayed? When is the delay observed? Who is causing more delays? Can we predict if the train is going to be delayed?

### Dependencies
Pandas, Numpy, Datetime, matplotlib.pyplot, seaborn, warnings, OSGB36toWGS84 from bng_latlon, sklearn, pyspark, sqlalchemy, psycopg2, json, glob, xml.etree.ElementTree, logging, time, Docker, Apache Kafka
### Executing program
1. **Kafka Zookeeper**: A service necessary for running the Kafka broker. It helps in maintaining the configuration information and provides distributed synchronization.
2. **Kafka Broker**: The heart of the Kafka system that maintains the published data. Each Kafka broker can handle terabytes of messages without performance impact.
3. **Kafka Producer (Python)**: This application pulls data from the National Rail APIs and publishes it to Kafka. It's designed to run indefinitely, continually pulling and publishing data.
4. **Kafka Consumer (Spark)**: A Spark application that consumes data from Kafka, processes it and writes the result to a PostgreSQL database.
5. **PostgreSQL Database (db)**: Stores the processed data from the Spark consumer for later analysis.
6. **EDA_proccess.ipynb**: Takes in data from the PostgreSQL database and cleans it and exports it to a csv file and also completes a data analysis, and data model prediction.
7. **RailData_analysis.pbix**: Takes in data from the csv file and performs analysis to answer our questions
### Authors

Ilackkeya Bhavananthi bsilackkeya21@gmail.com

Osman Nayeem osman_nayeem@yahoo.com 

Brian Levesque brian.lev722@gmail.com

### Acknowledgments

Our Grand Circus Instruction Team 

James Meredith, our main instructor

Dylan Gleason, our teaching assistant

Billy Westley, our program manager

