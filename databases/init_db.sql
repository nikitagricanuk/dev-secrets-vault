CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(60) NOT NULL,
    roles TEXT[] UNIQUE NOT NULL, -- roles the user belongs to, for example ('admin', 'dev', 'sysadmin')
    is_disabled BOOLEAN NOT NULL DEFAULT false, -- set if the account is disabled
    is_admin BOOLEAN NOT NULL DEFAULT false,
    expires_at TIMESTAMP, -- if set, set is_disabled to true
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE secrets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    secret_data jsonb NOT NULL,
    secret_data_history jsonb
);

CREATE TABLE settings (
    id SERIAL PRIMARY KEY,
    scope_type TEXT NOT NULL, -- type of scope, for example 'global' or 'user'
    scope UUID, -- settings scope, only use if scope_type is anything but global
    setting_key TEXT NOT NULL, -- store data in key - value format, like in redis
    setting_value jsonb NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE acl (
    id SERIAL PRIMARY KEY,
    resource_type TEXT NOT NULL, -- for example 'secret'
    resource_id INT NOT NULL,
    permission TEXT[] NOT NULL, -- for example ('read', 'write')
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);