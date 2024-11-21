#!/bin/bash

# Source the virtual environment
source .venv/bin/activate

# Run the manage.py script with any arguments passed to this script
python3 bend/manage.py "$@"