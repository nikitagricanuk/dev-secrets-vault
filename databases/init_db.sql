CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_disabled BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    role_name VARCHAR(255) UNIQUE NOT NULL,
);

CREATE TABLE secrets (
    id SERIAL PRIMARY KEY,
    group VARCHAR(255) NOT NULL,
    sectet_data jsonb NOT NULL, 
    secret_history jsonb
);