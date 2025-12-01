#!/bin/bash

export PORT=4000
export DEBUG=TRUE
export DB_FILENAME=database.db
export JWT_SECRET=secret


echo "Migration api ..."
./.venv/bin/python3 src/migrate.py

echo "Execute api ..."
./.venv/bin/python3 src/main.py

