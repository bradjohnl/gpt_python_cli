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

def continue_conversation():
    while True:
        user_input = input("Do you want to continue the conversation? (y/n): ").lower()
        if user_input in ('y', 'n'):
            return user_input == 'y'
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

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

messages = [{"role": "system", "content": "You are a helpful assistant."}]

if input_type == 'question':
    messages.append({"role": "user", "content": input_content})
elif input_type == 'code':
    messages.append({"role": "user", "content": f"{file_content}\n# {input_content}\n"})

while True:
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=2048,
        n=1,
        temperature=0.9,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " A:"]
    )

    response_text = response['choices'][0]['message']['content']
    print(response_text)

    if not continue_conversation():
        break

    messages.append({"role": "assistant", "content": response_text})
    user_input = input("Enter your next message: ")
    messages.append({"role": "user", "content": user_input})