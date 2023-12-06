from pyspark.sql import SparkSession
from pyspark.sql.functions import from_csv,from_json
from pyspark.sql.types import StructType, StructField, IntegerType,FloatType,DoubleType
from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import col


spark = SparkSession.builder \
    .appName("Project") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()




model = LogisticRegressionModel.load("models\logisticRegressionModel")



# Kafka'dan veri okuma
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "mobilPriceTopic") \
    .option("startingOffsets", "earliest") \
    .option("maxOffsetsPerTrigger", "1") \
    .load()




# df = df.selectExpr("CAST(value AS STRING) as value")

df = df.selectExpr("CAST(value AS STRING)")

parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .selectExpr("split(value, ',') AS data") \
    .selectExpr(
        "CAST(data[0] AS Float) AS battery_power",
        "CAST(data[1] AS Float) AS blue",
        "CAST(data[2] AS Double) AS clock_speed",
        "CAST(data[3] AS Float) AS dual_sim",
        "CAST(data[4] AS Float) AS fc",
        "CAST(data[5] AS Float) AS four_g",
        "CAST(data[6] AS Float) AS int_memory",
        "CAST(data[7] AS Double) AS m_dep",
        "CAST(data[8] AS Float) AS mobile_wt",
        "CAST(data[9] AS Float) AS n_cores",
        "CAST(data[10] AS Float) AS pc",
        "CAST(data[11] AS Float) AS px_height",
        "CAST(data[12] AS Float) AS px_width",
        "CAST(data[13] AS Float) AS ram",
        "CAST(data[14] AS Float) AS sc_h",
        "CAST(data[15] AS Float) AS sc_w",
        "CAST(data[16] AS Float) AS talk_time",
        "CAST(data[17] AS Float) AS three_g",
        "CAST(data[18] AS Float) AS touch_screen",
        "CAST(data[19] AS Float) AS wifi",
        "CAST(data[20] AS Float) AS price_range",
    )






vec = VectorAssembler(inputCols=['battery_power',
 'clock_speed',
 'fc',
 'int_memory',
 'm_dep',
 'mobile_wt',
 'pc',
 'px_height',
 'px_width',
 'ram',
 'sc_h',
 'sc_w',
 'talk_time',
 'four_g',
 'wifi',
 'three_g',
 'blue',
 'n_cores',
 'touch_screen',
 'dual_sim'],outputCol="features")
spark_df  = vec.transform(parsed_df)


df_with_predictions = model.transform(spark_df)

selected_df = df_with_predictions.select(col("battery_power"),col("clock_speed"),col("px_height"),col("wifi"),col("blue"),col("features"),col("rawPrediction"),col("probability") ,col("prediction"),col("price_range"))



query = selected_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .trigger(processingTime="2 seconds") \
    .start()


query.awaitTermination()