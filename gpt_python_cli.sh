#!/bin/bash

# activate the environment
source activate gpt_python_cli

# execute the script with all arguments passed to this script
python main.py "$@"

# deactivate the environment
conda deactivate
