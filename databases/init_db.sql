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
    tags TEXT[] NOT NULL, -- for example 'api_key' or 'password'
    secret_data jsonb NOT NULL,
    secret_data_history jsonb,
    secret_data_hashsum TEXT,
    is_disabled BOOLEAN NOT NULL DEFAULT false, -- set if the account is disabled
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    created_by VARCHAR(50) NOT NULL, -- username
    expires_at TIMESTAMP, -- if set, set is_disabled to true
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE settings (
    id SERIAL PRIMARY KEY,
    scope_type TEXT NOT NULL, -- type of scope, for example 'global' or 'user'
    scope UUID, -- settings scope, only use if scope_type is anything but global
    setting_key TEXT NOT NULL, -- store data in key - value format, like in redis
    setting_value jsonb NOT NULL,
    is_disabled BOOLEAN NOT NULL DEFAULT false, -- set if the account is disabled
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP, -- if set, set is_disabled to true,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE acl (
    id SERIAL PRIMARY KEY,
    resource_type TEXT NOT NULL, -- for example 'secret'
    resource_id INT NOT NULL,
    permission TEXT[] NOT NULL, -- for example ('read', 'write')
    is_disabled BOOLEAN NOT NULL DEFAULT false, -- set if the account is disabled
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    expires_at TIMESTAMP, -- if set, set is_disabled to true,
    updated_at TIMESTAMP DEFAULT NOW()
);