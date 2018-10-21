#!/usr/local/bin/bash

source venv/bin/activate

export FLASK_ENV=development
export DATABASE_URL="postgresql://bjaus@password@localhost:5432/starbooks"

python run.py

