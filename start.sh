#!/bin/bash
cd $(dirname $0)

if [ -z $VIRTUAL_ENV ]; then
  if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
  fi

  echo "Checking dependencies..."
  echo "Running game..."
  venv/bin/python src/main.py
else
  echo "Checking dependencies..."
  pip install -r requirements.txt

  echo "Running game..."
  python src/main.py
fi
