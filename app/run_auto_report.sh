#!/bin/bash
cd "$(dirname "$0")/.."
PYTHON_PATH=".venv/bin/python"
if [ ! -x "$PYTHON_PATH" ]; then
  PYTHON_PATH="python3"
fi
"$PYTHON_PATH" app/auto_report.py