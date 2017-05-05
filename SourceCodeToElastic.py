import os

from pyspark import SparkContext
from pyspark import SparkConf

inputFile = os.environ["SPARK_INPUT_FILE"]
indexName = os.environ["ELASTIC_INDEX_NAME"]
conf = SparkConf().setAppName("SourceCodeToElastic").setMaster("local[*]")
conf.set("es.index.auto.create", "true")
sc = SparkContext2(conf)
