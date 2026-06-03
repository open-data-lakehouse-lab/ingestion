#!/usr/bin/env bash
set -euo pipefail

echo "Running Ruff check..."
python3 -m ruff check .

echo "Running Mypy check..."
python3 -m mypy src

echo "Running Tests..."
python3 -m pytest
