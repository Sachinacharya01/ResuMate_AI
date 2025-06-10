#!/bin/bash

# Prevent Pytest from auto-loading external plugins or external conftest.py
#export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1

# Activate venv
source venv/bin/activate

# Set PYTHONPATH to current directory (project root)
export PYTHONPATH=$(pwd)

# Limit conftest.py search to this folder and below
pytest tests/ --confcutdir=$(pwd) --maxfail=2 --disable-warnings -v