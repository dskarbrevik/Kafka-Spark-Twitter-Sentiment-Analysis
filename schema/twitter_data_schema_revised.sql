
--Twitter Sentiment Analysis Schema
--UCB W205 Course Project
--Created By: Shuang Chan, David Skarbrevik
--Created On: 11/01/2016
--Target Environment: HIVE, SPARK

set hive.exec.dynamic.partition = true;
set hive.exec.dynamic.partition.mode=nonstrict;
set hive.mapred.supports.subdirectories=true;
set mapred.input.dir.recursive=true;

--Table to store the raw Twitter JSON data
drop table IF EXISTS twitter_raw_json;
create EXTERNAL table twitter_raw_json
(
        topic string,
        json_response string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
"separatorChar" = ",",
"quoteChar" = '"',
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/twitter/twitter-topic/';

--Table to store the results of the sentiment analysis
drop table IF EXISTS twitter_result;
CREATE EXTERNAL TABLE twitter_result
(
        topic string,
        sentiment string,
        created_at_dt timestamp,
        valid_words string
)
partitioned by (xdate date)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
"separatorChar" = ",",
"quoteChar" = '"',
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/twitter/twitter_result';






