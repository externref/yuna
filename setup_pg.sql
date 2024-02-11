CREATE TABLE IF NOT EXISTS confession_configs (
    guild_id BIGINT PRIMARY KEY,
    channel_id BIGINT 
);

CREATE TABLE IF NOT EXISTS confession_messages (
    id INTEGER ,
    message_content VARCHAR ,
    guild_id BIGINT ,
    user_id BIGINT ,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP    
);

CREATE TABLE IF NOT EXISTS confession_bans (
    user_id BIGINT ,
    guild_id BIGINT ,
    reason VARCHAR DEFAULT 'no reason provided'
);

CREATE TABLE IF NOT EXISTS member_logs (
    action VARCHAR ,
    guild_id BIGINT, 
    channel_id BIGINT,
    message VARCHAR,
    image_url VARCHAR DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS afk_data (
    user_id BIGINT,
    guild_id BIGINT,
    is_global BOOLEAN,
    message VARCHAR,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS afk_mentions (
    user_id BIGINT,
    guild_id BIGINT,
    mention_msg VARCHAR,
    mention_url VARCHAR,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);