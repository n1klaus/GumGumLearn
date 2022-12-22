#!/usr/bin/bash
# Delete existing resources and create new ones for development
cat backend/database/setup_db_dev.sql | psql postgres postgres
