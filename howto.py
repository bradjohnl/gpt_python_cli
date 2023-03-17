#!/usr/bin/env python3

import os
import openai
import sys

openai.api_key = os.environ.get('OPENAI_API_KEY')

def print_help():
    print("Usage:")
    print("  --question, -q <question>         Ask a generic question")
    print("  --code, -c <code>                 Generate code based on the given text")
    print("  --model, -m <model>               Specify the model to use (gpt-4 or gpt-4-32k)")
    print("  --file, -f <file_path>            Use a file as input for the model")
    print("  --help, -h                        Show this help message")

input_type = None
input_content = sys.argv[1]
model = None
file_content = None
file_path = None

for i, arg in enumerate(sys.argv[1:]):
    if arg in ('--help', '-h'):
        print_help()
        sys.exit(0)
    elif arg in ('--question', '-q'):
        input_type = 'question'
        input_content = sys.argv[i + 2]
    elif arg in ('--code', '-c'):
        input_type = 'code'
        input_content = sys.argv[i + 2]
    elif arg in ('--model', '-m'):
        model = sys.argv[i + 2]
        if model not in ["gpt-4", "gpt-4-32k"]:
            print("Invalid model. Choose 'gpt-4' or 'gpt-4-32k'.")
            sys.exit(1)
    elif arg in ('--file', '-f'):
        file_path = sys.argv[i + 2]

if model is None:
    model = "gpt-4-32k" if input_type == "code" else "gpt-4"

if file_path:
    with open(file_path, 'r') as file:
        file_content = file.read()

if input_type == 'question':
    prompt = f"""Q: {input_content}
A:"""
elif input_type == 'code':
    prompt = f"# {input_content}\n\n{file_content}\n"
else:
    prompt = f"Convert this text to a linux shell command.\n\nExample: Show all filesystems usage, space and mount point in human format\nOutput: df -h\n\nExample: Check the size of the pCloudDrive folder every 3 seconds\nOutput: while true; do du -sh pCloudDrive; sleep 1s; clear; done;\n\nExample: Find the smallest file in a directory and in all its subdirectories\nOutput: find . -type f -exec du -sh {{}} + | sort -n\nExample: {input_content}\nOutput:"

max_tokens = 2048 if model == "gpt-4" else 32000

response = openai.ChatCompletion.create(
    model=model,
    messages=[{"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": prompt}],
    max_tokens=max_tokens,
    n=1,
    temperature=0.9,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=["\n", " A:"]
)

response_text = response['choices'][0]['message']['content']
print(response_text)
