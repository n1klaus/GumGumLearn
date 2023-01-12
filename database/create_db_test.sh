#!/usr/bin/bash
# Delete existing resources and create new ones for testing
cat setup_db_test.sql | psql postgres postgres
