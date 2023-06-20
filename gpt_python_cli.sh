#!/bin/bash

# Get the directory of the current script
DIR="$(dirname "$(readlink -f "$0")")"

# activate the environment
source activate gpt_python_cli

# execute the script with all arguments passed to this script
python "$DIR/main.py" "$@"

# deactivate the environment
conda deactivate

