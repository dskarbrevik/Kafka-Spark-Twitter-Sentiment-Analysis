
#! /bin/bash

#UBS W205 Course Project
#Upload Sentiment Analysis To S3
#Created By: Shuang Chan, David Skarbrevik
#Created On: 11/01/2016

# Require AWS CLI
# Require Access Key ID and Secret Access Key
# To obtain Access Key ID and Secret Access Key
# follow the instruction in http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html

# $pip install awscli
# $aws configure

# Clean up files
rm -r twitter_result.tar
rm -r twitter_result

# Download data from HDFS
mkdir twitter_result
hdfs dfs -get /user/w205/twitter/twitter_result/* twitter_result

# Compress data
tar -cf twitter_result.tar twitter_result

# Upload data to S3
aws s3 cp twitter_result.tar s3://w205sentimentanalysis/twitter_result.tar

