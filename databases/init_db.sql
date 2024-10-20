CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;

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
    secret_data TEXT NOT NULL,
    secret_data_history TEXT,
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

CREATE TABLE userkeys (
  username varchar(50),
  crypto_key text,
  created_at TIMESTAMP DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE secret_history (
  id UUID NOT NULL,
  name VARCHAR(50) UNIQUE NOT NULL,
  description TEXT,
  tags TEXT[] NOT NULL, -- for example 'api_key' or 'password'
  secret_data TEXT NOT NULL,
  secret_data_hashsum TEXT,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- name, description, tags, secret_data, created_by, expires_at

CREATE FUNCTION create_secret(
    _name VARCHAR(50),
    _description TEXT,
    _tags TEXT[],
    _secret_data jsonb,
    _created_by VARCHAR(50), -- username
    _expires_at TIMESTAMP -- if set, set is_disabled to true
    ) RETURNS BOOLEAN
 LANGUAGE plpgsql AS
$$
DECLARE
   _some_key text;
   _scrypd text;
   _hashsum text;
BEGIN
  if EXISTS(select crypto_key from userkeys where username = _created_by) then
    select crypto_key from userkeys where username = _created_by into _some_key;
  else
    _some_key := gen_random_bytes(16);
    insert into userkeys values (_created_by, _some_key);
  end if;
  _scrypd := pgp_sym_encrypt(cast(_secret_data as text), _some_key);
  _hashsum := md5(_scrypd);
  insert into secrets (name, description, tags, secret_data, secret_data_hashsum, created_by, expires_at) 
    values (_name, _description, _tags, _scrypd, _hashsum, _created_by, _expires_at);
  RETURN TRUE;
END
$$;

CREATE FUNCTION get_secret(
    _id UUID DEFAULT uuid_generate_v4(),
    _name VARCHAR(50) DEFAULT ''
) RETURNS TABLE (
    id UUID,
    name VARCHAR(50),
    description TEXT,
    tags TEXT[], -- for example 'api_key' or 'password'
    secret_data TEXT,
    secret_data_history TEXT,
    secret_data_hashsum TEXT,
    is_disabled BOOLEAN, -- set if the account is disabled
    created_at TIMESTAMP,
    created_by VARCHAR(50), -- username
    expires_at TIMESTAMP, -- if set, set is_disabled to true
    updated_at TIMESTAMP
)
  LANGUAGE plpgsql AS
$$
BEGIN
  RETURN QUERY SELECT * FROM secrets WHERE secrets.id = _id OR secrets.name = _name;
END;
$$;

CREATE FUNCTION update_secret(
    _id UUID,
    _name VARCHAR(50),
    _description TEXT,
    _tags TEXT[],
    _secret_data jsonb,
    _created_by VARCHAR(50), -- username
    _expires_at TIMESTAMP -- if set, set is_disabled to true
    ) RETURNS BOOLEAN
 LANGUAGE plpgsql AS
$$
DECLARE
   _some_key text;
   _scrypd text;
   _hashsum text;
BEGIN
  IF _id IS NULL AND _name IS NULL then
    RETURN FALSE;
  END IF;

  if EXISTS(select crypto_key from userkeys where username = _created_by) then
    select crypto_key from userkeys where username = _created_by into _some_key;
  else
    _some_key := gen_random_bytes(16);
    insert into userkeys values (_created_by, _some_key);
  end if;
  
  INSERT INTO secret_history (id, name, description, tags, secret_data, secret_data_hashsum)
  select id, name, description, tags, secret_data, secret_data_hashsum from secrets
  where secrets.id = _id OR secrets.name = name;
  
  _scrypd := pgp_sym_encrypt(cast(_secret_data as text), _some_key);
  _hashsum := md5(_scrypd);
  update secrets set (name, description, tags, secret_data, secret_data_hashsum, created_by, expires_at) 
    = (_name, _description, _tags, _scrypd, _hashsum, _created_by, _expires_at)
    where secrets.name = _name OR secrets.id = _id;
  
  RETURN TRUE;
END
$$;