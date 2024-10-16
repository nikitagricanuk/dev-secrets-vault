CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    roles TEXT[] UNIQUE NOT NULL, -- roles the user belongs to, for example ('admin', 'dev', 'sysadmin')
    is_disabled BOOLEAN NOT NULL DEFAULT false, -- set if the account is disabled
    expires_at TIMESTAMP, -- if set, set is_disabled to true
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE secrets (
    id SERIAL PRIMARY KEY,
    secret_data jsonb NOT NULL
);

CREATE TABLE settings (
    id SERIAL PRIMARY KEY,
    scope TEXT NOT NULL, -- settings scope, for example global for all users, or user:uid for specific user
    setting_key TEXT NOT NULL, -- store data in key - value format, like in redis
    setting_value JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE acl (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    resource_type TEXT NOT NULL,
    resource_id INT NOT NULL,
    permission TEXT[] NOT NULL, -- for example ('read', 'write')
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);