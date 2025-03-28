#!/bin/bash
cd "$(dirname "$0")" || exit

if [ -z "$VIRTUAL_ENV" ]; then
  if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
  fi

  echo "Checking dependencies..."
  venv/bin/pip install -r requirements.txt

  echo "Running game..."
  venv/bin/python src/main.py
else
  echo "Checking dependencies..."
  pip install -r requirements.txt

  echo "Running game..."
  python src/main.py
fi
