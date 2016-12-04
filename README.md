# MIDSW205_Project - Political Sentiment Analysis
MIDS W205 Group Project (Section 4 - David Skarbrevik and Shuang Chan)

Prerequisites:

1. Hadoop 2.6
2. Spark 1.5
3. Python 3.4 (with NLTK, Numpy and Tweepy libraries)
4. Kafka
5. AWS CLI

Installation:

1. Download https://github.com/dskarby/MIDSW205_Project
2. Start HIVE
3. hive> create database twitter
4. hive> use twitter;
5. Run twitter_data_schema_revised.sql

Create Sentiment Corpus:

$ python3.4 build_sentiment_corpus.py

Run Sentiment Analysis:

$ PYSPARK_PYTHON=python3.4 /data/spark15/bin/spark-submit sentiment_analysis_revised.py

Upload Sentiment Analysis Data to S3:

$ ./upload_s3.sh





