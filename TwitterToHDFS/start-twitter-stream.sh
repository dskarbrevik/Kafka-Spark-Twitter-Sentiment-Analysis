#!/bin/bash

# This file executes all the necessary processes to stream Tweets and save them in HDFS

cwd=$(pwd) # working dir for this project

#******
cd /home/w205/CourseProject/programs/kafka_2.11-0.10.1.0/ # EDIT THIS PATH TO POINT AT YOUR KAFKA DIRECTORY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
bash ./bin/zookeeper-server-start.sh ./config/zookeeper.properties &
echo $! # show process id for zookeeper
sleep 15
#******

bash ./bin/kafka-server-start.sh ./config/server.properties & # starts the kafka server
echo $! # show process id for kafka server
sleep 15

cd $cwd/kafka-topics/topic-hillary/
mvn exec:java & #starts kafka producer on twitter topic Hillary
echo $! # show process id
sleep 15

cd $cwd/kafka-topics/topic-trump/ 
mvn exec:java & # starts kafka producer on twitter topic Trump
echo $!
sleep 15

cd $cwd
hadoop jar camus-SNAPSHOT-shaded.jar com.linkedin.camus.etl.kafka.CamusJob -P camus.properties # feeds kafka/twitter stream to hdfs

