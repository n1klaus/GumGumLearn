-- create database and user for test environment
REASSIGN OWNED BY learn_test TO postgres;
DROP OWNED BY learn_test;
DROP USER IF EXISTS learn_test;
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
COMMENT ON SCHEMA public IS 'standard public schema';
DROP DATABASE IF EXISTS learn_test_db;

CREATE USER learn_test WITH password 'learn_test_pwd' CREATEDB CREATEROLE;
CREATE DATABASE learn_test_db
	TEMPLATE template0
	OWNER learn_test
	ENCODING 'utf8'
	LC_COLLATE 'en_US.utf8'
	LC_CTYPE 'en_US.utf8';

ALTER SCHEMA public OWNER to postgres;
GRANT ALL PRIVILEGES ON DATABASE learn_test_db to learn_test;
GRANT USAGE, CREATE ON SCHEMA public TO learn_test;
