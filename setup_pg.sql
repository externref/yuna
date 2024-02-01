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