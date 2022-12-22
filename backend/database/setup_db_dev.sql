-- create database and user for development environment
REASSIGN OWNED BY learn_dev TO postgres;
DROP OWNED BY learn_dev;
DROP SCHEMA public CASCADE;
DROP USER IF EXISTS learn_dev;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
COMMENT ON SCHEMA public IS 'standard public schema';
DROP DATABASE IF EXISTS learn_dev_db;

CREATE USER learn_dev WITH password 'learn_dev_pwd' CREATEDB CREATEROLE;
CREATE DATABASE learn_dev_db
	TEMPLATE template0
	OWNER learn_dev
	ENCODING 'utf8'
	LC_COLLATE 'en_US.utf8'
	LC_CTYPE 'en_US.utf8';

ALTER SCHEMA public OWNER to postgres;
GRANT ALL PRIVILEGES ON DATABASE learn_dev_db to learn_dev;
GRANT USAGE, CREATE ON SCHEMA public TO learn_dev;
