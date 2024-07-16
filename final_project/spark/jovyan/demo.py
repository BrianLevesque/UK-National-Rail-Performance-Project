import pyspark
from pyspark.sql import SparkSession

BOOTSTRAP_SERVERS = "localhost:9092,broker:29092"
TOPIC = "darwin"

def main():
    spark = SparkSession.builder.master("local[1]") \
                        .appName('OvenTempReader') \
                        .getOrCreate()

    df = spark \
      .readStream \
      .format("kafka") \
      .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
      .option("session.timeout.ms", "45000") \
      .option("subscribe", TOPIC) \
      .load()
    
    query = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
            .writeStream \
            .outputMode("append") \
            .format("console") \
            .start()

    query.awaitTermination()
    
if __name__ == "__main__":
    main()
