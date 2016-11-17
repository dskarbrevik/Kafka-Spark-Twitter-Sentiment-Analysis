
set hive.exec.dynamic.partition = true;
set hive.exec.dynamic.partition.mode=nonstrict;

--Load sample Twitter JSON data into the twitter_raw_json table
--Note: need to upload the data file to HDFS first

load data inpath '/user/w205/twitter/sample_twitter_data.json'
into table twitter_raw_json
partition (batchid = 1);

--Tranform the JSON data and load into the twitter_structured_data table
from twitter_raw_json
insert overwrite table twitter_structured_data
partition (batchid)
select
        cast(get_json_object(json_response, '$.id_str') as bigint),
        to_utc_timestamp(concat
        (
        substr (get_json_object(json_response, '$.created_at'),27,4),
        '-',
        (case substr (get_json_object(json_response, '$.created_at'),5,3)
                when "Jan" then "01"
                when "Feb" then "02"
                when "Mar" then "03"
                when "Apr" then "04"
                when "May" then "05"
                when "Jun" then "06"
                when "Jul" then "07"
                when "Aug" then "08"
                when "Sep" then "09"
                when "Oct" then "10"
                when "Nov" then "11"
                when "Dec" then "12" end),
        '-',
        substr (get_json_object(json_response, '$.created_at'),9,2),
        ' ',
        substr (get_json_object(json_response, '$.created_at'),12,8)
        ), 'UTC'),
        get_json_object(json_response, '$.in_reply_to_user_id_str'),
        regexp_replace(regexp_replace(trim(lower(get_json_object(json_response, '$.text'))), '\\n', ' '), '\\r', ' '),
        get_json_object(json_response, '$.contributors'),
        get_json_object(json_response, '$.retweeted'),
        get_json_object(json_response, '$.truncated'),
        get_json_object(json_response, '$.coordinates'),
        get_json_object(json_response, '$.source'),
        cast (get_json_object(json_response, '$.retweet_count') as int),
        regexp_replace(regexp_replace(trim(lower(get_json_object(json_response, '$.entities.hashtags[0].text'))), '\\n', ' '), '\\r', ' '),
        trim(lower(get_json_object(json_response, '$.entities.user_mentions[0].screen_name'))),
        get_json_object(json_response, '$.user.screen_name'),
        get_json_object(json_response, '$.user.name'),
        cast (get_json_object(json_response, '$.user.followers_count') as int),
        cast (get_json_object(json_response, '$.user.listed_count') as int),
        cast (get_json_object(json_response, '$.user.friends_count') as int),
        get_json_object(json_response, '$.user.lang'),
        get_json_object(json_response, '$.user.location'),
        get_json_object(json_response, '$.user.time_zone'),
        batchid
where (length(json_response) > 0);

--Rebuild Index
ALTER INDEX idx_created_at_dt_01 ON twitter_structured_data REBUILD;

