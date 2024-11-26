#!/bin/sh
set -e

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating one..."
    uv venv -p 3.12 .venv
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists."
fi

. .venv/bin/activate

uv pip install -U syftbox torch --quiet

# run app using python from venv
echo "Running pretrained_model_aggregator with $(python3 --version) at '$(which python3)'"
python3 main.py

# deactivate the virtual environment
deactivate