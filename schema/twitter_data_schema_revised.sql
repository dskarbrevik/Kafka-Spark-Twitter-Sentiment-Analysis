
--Create Twitter Raw JSON table
drop table IF EXISTS twitter_raw_json;
create table twitter_raw_json
(
        json_response string
) 
partitioned by (batchid int);

--Create Twitter Structured Data table
drop table IF EXISTS twitter_structured_data;
create table twitter_structured_data
(
        id bigint,
        created_at_dt timestamp,
        in_reply_to_user_id_str string,
        text string,
        contributors string,
        retweeted string,
        truncated string,
        coordinates string,
        source string,
        retweet_count int,
        first_hashtag string,
        first_user_mention string,
        screen_name string,
        name string,
        followers_count int,
        listed_count int,
        friends_count int,
        lang string,
        user_location string,
        time_zone string
)
partitioned by (batchid int);

CREATE INDEX idx_created_at_dt_01 ON TABLE twitter_structured_data (created_at_dt) AS 'COMPACT' WITH DEFERRED REBUILD;





