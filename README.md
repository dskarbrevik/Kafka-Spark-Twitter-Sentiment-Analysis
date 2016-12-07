# MIDSW205_Project - Political Sentiment Analysis
MIDS W205 Group Project (Section 4 - David Skarbrevik and Shuang Chan)

## Prerequisites:

1. Apache Zookeeper
2. Apache Maven 2/3
3. Hadoop 2.6
4. Spark 1.5
5. Python 3.4 (with NLTK, Numpy and Tweepy libraries)
6. Apache Kafka 0.8
7. Oracle JDK 1.7 (64 bit)
8. AWS CLI

Complete the following phases in listed order:

## Installation:

1. Make sure you are root user (not absolutely necessary, but you will need to do an extra step if not).
2. Download https://github.com/dskarby/MIDSW205_Project.
3. Make sure the path variable is set for Apache Maven .
  ("find / -name mvn" to find path or verify path is set using "mvn -v").
4. CD into TwitterToHDFS directory of this project
5. vim start-twitter-stream.sh and edit the line with comment "EDIT THIS PATH" so it points at your Apach Kafka directory (if using our ec2 instance, this is already set correctly).
6. [if not root user] vim camus.config and edit the three path variables (top of file) by changing the part of the current path that says "root" to whatever your current username is.

## Get Twitter Data:

1. Make sure you're in "TwitterToHDFS" directory
2. Run start-twitter-stream.sh (this will take 2-3 minutes).

At this point a few minutes worth of twitter data will be uploaded to Amazon S3. Kafka will still be running. If you would like to send more of the data Kafka is collecting to HDFS you can run the following command as often as you would like (though we recommend once every 2 hours... be aware of how quickly hard drive space is taken up) "hadoop jar camus-SNAPSHOT-shaded.jar com.linkedin.camus.etl.kafka.CamusJob -P camus.properties". Note that this command must be executed while in our main project directory.

## Make Hive Table:

1. Start HIVE
2. hive> create database twitter
3. hive> use twitter;
4. Run twitter_data_schema_revised.sql

## Create Sentiment Corpus:

$ python3.4 build_sentiment_corpus.py

## Run Sentiment Analysis:

$ PYSPARK_PYTHON=python3.4 /data/spark15/bin/spark-submit sentiment_analysis_revised.py

## Upload Sentiment Analysis Data to S3:

$ ./upload_s3.sh

At this point you have sent fully analyzed Twitter data to Amazon S3.






