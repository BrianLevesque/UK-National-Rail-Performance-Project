from pyspark.sql import SparkSession

BOOTSTRAP_SERVERS = "localhost:9092,broker:29092"
TOPIC = "darwin"
CHECKPOINT_LOCATION = "checkpoint_xml"
EXPORT_PATH = "xml"

def get_spark_session(app_name, master="local[1]"):
    return SparkSession.builder.master(master).appName(app_name).getOrCreate()

def read_kafka_stream(spark, servers, topic):
    df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", servers).option("subscribe", topic).load()
    return df.selectExpr("CAST(value AS STRING)")

def write_stream_to_parquet(df, export_path, checkpoint_location):
    query = df.writeStream.outputMode("append").format("parquet").option("path", export_path).option("checkpointLocation", checkpoint_location).start()
    return query

def main():
    spark = get_spark_session('NationalRailData')
    df = read_kafka_stream(spark, BOOTSTRAP_SERVERS, TOPIC)
    
    query = write_stream_to_parquet(df, EXPORT_PATH, CHECKPOINT_LOCATION)
    query.awaitTermination()

if __name__ == "__main__":
    main()
