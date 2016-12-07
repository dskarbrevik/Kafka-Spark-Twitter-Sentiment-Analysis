# MIDSW205_Project - Political Sentiment Analysis
MIDS W205 Group Project (Section 4 - David Skarbrevik and Shuang Chan)

Prerequisites:

1. Apache Zookeeper
2. Apache Maven 2/3
3. Hadoop 2.6
4. Spark 1.5
5. Python 3.4 (with NLTK, Numpy and Tweepy libraries)
6. Apache Kafka 0.8
7. Oracle JDK 1.7 (64 bit)
8. AWS CLI

Installation:

1. Make sure you are root user (not absolutely necessary, but you will need to do an extra step)
2. Download https://github.com/dskarby/MIDSW205_Project
3. Make sure the path variable is set for Apache Maven 
  ("find / -name mvn" to find path or verify path is set using "mvn -v")
4. CD into project directory
5. vim start-twitter-stream.sh and edit the line with comment "EDIT THIS PATH" so it points at your Apach Kafka directory
6. [if not root user] vim camus.config and edit the three path variables (top of file) by changing the part of the current path that says "root" to whatever your current username is.
7. Run start-twitter-stream.sh (this will take 2-3 minutes)
8. Start HIVE
9. hive> create database twitter
10. hive> use twitter;
11. Run twitter_data_schema_revised.sql

Create Sentiment Corpus:

$ python3.4 build_sentiment_corpus.py

Run Sentiment Analysis:

$ PYSPARK_PYTHON=python3.4 /data/spark15/bin/spark-submit sentiment_analysis_revised.py

Upload Sentiment Analysis Data to S3:

$ ./upload_s3.sh

** At this point a few minutes worth of twitter data will be uploaded to Amazon S3






