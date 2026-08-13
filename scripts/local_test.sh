#!/usr/bin/env bash

set -e

echo "🔍 Running pre-push checks & tests..."

# Ensure we are in project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

echo "1. Checking Python dependencies..."
python3 -m pip install -q flake8 pytest

echo "2. Running Flake8 syntax checks..."
python3 -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

echo "3. Running Pytest suite..."
python3 -m pytest tests/ -v

echo "✅ All checks passed successfully! Safe to git push to GitHub."
