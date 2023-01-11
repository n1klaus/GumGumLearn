#!/usr/bin/env bash
# Fix python scripts styling with autopep8 guidelines and pycodestyle style guide
VENV='./env/*'

if [ ! -f -s -e -x "w3c_validator.py" ]
then
    echo "Missing file, please try again..."
    exit
fi

echo "Running w3c html validator ..."
find . -type f -name '*.html' ! -path '*/node_modules/*' -exec python3 w3c_validator.py '{}' \;

echo "Running w3c css validator ..."
find . -type f -name '*.css' ! -path '*/node_modules/*' -exec python3 w3c_validator.py '{}' \;
