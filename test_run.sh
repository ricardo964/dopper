#!/bin/bash

export PORT=4000
export DEBUG=True
export DB_FILENAME=database.db
export JWT_SECRET=secret

if [ "$1" == "-m" ]; then
    echo "Execute migration ..."
    ./.venv/bin/python3 src/migrate.py
else
    echo "Execute api ..."
    ./.venv/bin/python3 src/main.py
fi
