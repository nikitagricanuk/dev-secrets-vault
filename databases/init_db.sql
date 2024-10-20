CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(60) NOT NULL,
    roles TEXT[] UNIQUE NOT NULL, -- roles the user belongs to, for example ('admin', 'dev', 'sysadmin')
    is_disabled BOOLEAN NOT NULL DEFAULT false, -- SET IF the account is disabled
    is_admin BOOLEAN NOT NULL DEFAULT false,
    expires_at TIMESTAMP, -- IF SET, SET is_disabled to true
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    UPDATEd_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE secrets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    tags TEXT[] NOT NULL, -- for example 'api_key' or 'password'
    secret_data TEXT NOT NULL,
    secret_data_history TEXT,
    secret_data_hashsum TEXT,
    is_disabled BOOLEAN NOT NULL DEFAULT false, -- SET IF the account is disabled
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    created_by VARCHAR(50) NOT NULL, -- username
    expires_at TIMESTAMP, -- IF SET, SET is_disabled to true
    UPDATEd_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE acl (
    id SERIAL PRIMARY KEY,
    resource_type TEXT NOT NULL, -- for example 'secret'
    resource_id INT NOT NULL,
    permission TEXT[] NOT NULL, -- for example ('read', 'write')
    is_disabled BOOLEAN NOT NULL DEFAULT false, -- SET IF the account is disabled
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    expires_at TIMESTAMP, -- IF SET, SET is_disabled to true,
    UPDATEd_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE userkeys (
  username varchar(50),
  crypto_key TEXT,
  created_at TIMESTAMP DEFAULT NOW() NOT NULL,
  UPDATEd_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE secret_history (
  id UUID NOT NULL,
  name VARCHAR(50) UNIQUE NOT NULL,
  description TEXT,
  tags TEXT[] NOT NULL, -- for example 'api_key' or 'password'
  secret_data TEXT NOT NULL,
  secret_data_hashsum TEXT,
  UPDATEd_at TIMESTAMP DEFAULT NOW()
);

-- name, description, tags, secret_data, created_by, expires_at

CREATE FUNCTION create_secret(
    _name VARCHAR(50),
    _description TEXT,
    _tags TEXT[],
    _secret_data jsonb,
    _created_by VARCHAR(50), -- username
    _expires_at TIMESTAMP -- IF SET, SET is_disabled to true
    ) RETURNS UUID
 LANGUAGE plpgsql AS
$$
DECLARE
   _id UUID;
   _some_key TEXT;
   _scrypd TEXT;
   _hashsum TEXT;
BEGIN
  IF EXISTS(SELECT crypto_key FROM userkeys WHERE username = _created_by) THEN
    SELECT crypto_key FROM userkeys WHERE username = _created_by INTO _some_key;
  ELSE
    _some_key := gen_random_bytes(16);
    INSERT INTO userkeys VALUES (_created_by, _some_key);
  END IF;
  _scrypd := pgp_sym_encrypt(cast(_secret_data as TEXT), _some_key);
  _hashsum := md5(_scrypd);
  INSERT INTO secrets (name, description, tags, secret_data, secret_data_hashsum, created_by, expires_at) 
    VALUES (_name, _description, _tags, _scrypd, _hashsum, _created_by, _expires_at)
  RETURNING id INTO _id;
  RETURN _id;
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
    is_disabled BOOLEAN, -- SET IF the account is disabled
    created_at TIMESTAMP,
    created_by VARCHAR(50), -- username
    expires_at TIMESTAMP, -- IF SET, SET is_disabled to true
    UPDATEd_at TIMESTAMP
)
  LANGUAGE plpgsql AS
$$
BEGIN
  RETURN QUERY SELECT * FROM secrets WHERE secrets.id = _id OR secrets.name = _name;
END;
$$;

CREATE FUNCTION UPDATE_secret(
    _id UUID,
    _name VARCHAR(50),
    _description TEXT,
    _tags TEXT[],
    _secret_data jsonb,
    _created_by VARCHAR(50), -- username
    _expires_at TIMESTAMP -- IF SET, SET is_disabled to true
    ) RETURNS BOOLEAN
 LANGUAGE plpgsql AS
$$
DECLARE
   _some_key TEXT;
   _scrypd TEXT;
   _hashsum TEXT;
BEGIN
  IF _id IS NULL AND _name IS NULL THEN
    RETURN FALSE;
  END IF;

  IF EXISTS(SELECT crypto_key FROM userkeys WHERE username = _created_by) THEN
    SELECT crypto_key FROM userkeys WHERE username = _created_by INTO _some_key;
  ELSE
    _some_key := gen_random_bytes(16);
    INSERT INTO userkeys VALUES (_created_by, _some_key);
  END IF;
  
  INSERT INTO secret_history (id, name, description, tags, secret_data, secret_data_hashsum)
  SELECT id, name, description, tags, secret_data, secret_data_hashsum FROM secrets
  WHERE secrets.id = _id OR secrets.name = name;
  
  _scrypd := pgp_sym_encrypt(cast(_secret_data as TEXT), _some_key);
  _hashsum := md5(_scrypd);
  UPDATE secrets SET (name, description, tags, secret_data, secret_data_hashsum, created_by, expires_at) 
    = (_name, _description, _tags, _scrypd, _hashsum, _created_by, _expires_at)
    WHERE secrets.name = _name OR secrets.id = _id;
  
  RETURN TRUE;
END
$$;