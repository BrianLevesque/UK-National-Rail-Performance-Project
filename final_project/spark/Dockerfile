## Use Pyspark notebook from Jupyter
FROM jupyter/pyspark-notebook

## Install Kafka JARs for Spark 
COPY jars/spark-streaming-kafka-0-10_2.12-3.3.2.jar /usr/local/spark/jars/
COPY jars/spark-sql-kafka-0-10_2.12-3.3.2.jar /usr/local/spark/jars/
COPY jars/kafka-clients-3.4.0.jar /usr/local/spark/jars/
COPY jars/spark-token-provider-kafka-0-10_2.12-3.3.2.jar /usr/local/spark/jars/
COPY jars/commons-pool2-2.11.1.jar /usr/local/spark/jars/

## Using Python 3 install requirements file
COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt
