#!/bin/bash

# Set environment variables for PostgreSQL
export POSTGRES_USER=fnas
export POSTGRES_PASSWORD=yourpassword
export POSTGRES_DB=db


(cd hello && flask run --host=0.0.0.0 --port=5000 &)

(cd http && flask run --host=0.0.0.0 --port=5001 &)

(cd assets && flask run --host=0.0.0.0 --port=5002 &)

(cd database && flask initdb && flask run --host=0.0.0.0 --port=5003 &)

(cd cache && flask run --host=0.0.0.0 --port=5004 &)

(cd form && flask run --host=0.0.0.0 --port=5005 &)

(cd template && flask run --host=0.0.0.0 --port=5006 &)

# Keep the container running
tail -f /dev/null
