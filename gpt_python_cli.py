#!/usr/bin/env python3

from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
import os
import openai
import sys
import json
import pathlib
from datetime import datetime

openai.api_key = os.environ.get('OPENAI_API_KEY')

def print_help():
    print("Usage:")
    print("  --question, -q <question>         Ask a generic question")
    print("  --model, -m <model>               Specify the model to use (gpt-4 only for the moment)")
    print("  --file, -f <file_path>            Use a file as input for the model")
    print("  --prompt, -p <prompt_name>        Use a custom prompt from the library")
    print("  --print-only, -po                 Print the command without asking to continue")
    print("  --save-log, -sl                   Save the chat log to a default path")
    print("  --tokens, -t <tokens>             Specify the number of tokens to use (default: 2000)")
    print("  --library-path, -lp <path>        Specify the docs library path for custom data (Other parameters except -q will not work when using custom data at the moment)")
    print("  --index-path, -ip <path>          Specify the index path for custom data (Other parameters except -q will not work when using custom data at the moment)")
    print("  --help, -h                        Show this help message")

def continue_conversation():
    while True:
        user_input = input("Do you want to continue the conversation? (y/n): ").lower()
        if user_input in ('y', 'n'):
            return user_input == 'y'
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def load_config():
    config_path = os.path.expanduser('~/.gpt_python_cli/config.json')
    with open(config_path) as file:
        return json.load(file)

def load_prompt(prompt_name, library_path):
    json_prompt_file = os.path.join(library_path, f"{prompt_name}.json")
    txt_prompt_file = os.path.join(library_path, f"{prompt_name}.txt")

    if os.path.isfile(json_prompt_file):
        with open(json_prompt_file, 'r') as file:
            return json.load(file)
    elif os.path.isfile(txt_prompt_file):
        with open(txt_prompt_file, 'r') as file:
            return file.read()
    else:
        raise FileNotFoundError(f"Prompt file not found: {prompt_name}.json or {prompt_name}.txt")

      
def get_standard_response(prompt, model, openai, tokens):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=0,
        max_tokens=tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=[" A:"]
    )
    return response.choices[0].text.strip()
  
def get_chat_response(messages, model, openai, tokens):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=tokens,
        n=1,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=[" A:"]
    )
    return response['choices'][0]['message']['content']
  

def construct_index(directory_path, index_path):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk(index_path)

    return index
  
def get_custom_data_response(input_text, index_path):
    index = GPTSimpleVectorIndex.load_from_disk(index_path)
    response = index.query(input_text, response_mode="compact")
    return response.response

def is_list_of_dicts(obj):
    return isinstance(obj, list) and all(isinstance(item, dict) for item in obj)

def format_list_of_dicts(list_of_dicts, input_content, file_content):
    formatted_list = []
    for item in list_of_dicts:
        formatted_item = {}
        for key, value in item.items():
            formatted_item[key] = value.format(input_content=input_content, file_content=file_content)
        formatted_list.append(formatted_item)
    return formatted_list

config = load_config()
default_library_path = config.get('library_path', '')

input_type = None
input_content = sys.argv[1]
model = None
file_content = None
file_path = None
custom_prompt = None
print_only = False
save_log = False
prompt_name = None
tokens = 2000
custom_data = False
custom_data_path = None
custom_data_index_path = None
messages = [{"role": "system", "content": "You are a helpful assistant."}]

i = 1
while i < len(sys.argv):
    arg = sys.argv[i]

    if arg in ('--help', '-h'):
        print_help()
        sys.exit(0)
    elif arg in ('--question', '-q'):
        input_type = 'question'
        input_content = sys.argv[i + 1]
        i += 1
    elif arg in ('--model', '-m'):
        model = sys.argv[i + 1]
        if model not in config['models']:
            print("Invalid model")
            sys.exit(1)
        model = config['models'][model]
        i += 1
    elif arg in ('--file', '-f'):
        file_path = sys.argv[i + 1]
        i += 1
    elif arg in ('--prompt', '-p'):
        prompt_name = sys.argv[i + 1]
        custom_prompt = load_prompt(sys.argv[i + 1], default_library_path)
        i += 1
    elif arg in ('--print-only', '-po'):
        print_only = True
    elif arg in ('--save-log', '-sl'):
        save_log = True
    elif arg in ('--tokens', '-t'):
        tokens = int(sys.argv[i + 1])
        i += 1
    elif arg in ('--library-path', '-lp'):
        custom_data = True
        custom_data_path = sys.argv[i + 1]
        i += 1
    elif arg in ('--index-path', '-ip'):
        custom_data = True
        custom_data_index_path = sys.argv[i + 1]
        i += 1
    else:
        print(f"Unknown option '{arg}'")
        print_help()
        sys.exit(1)
    
    i += 1

if model is None:
    model = "gpt-4"

if file_path:
    with open(file_path, 'r') as file:
        file_content = file.read()

if custom_prompt:
    if is_list_of_dicts(custom_prompt):
        custom_list_of_dicts = custom_prompt
        formatted_list_of_dicts = format_list_of_dicts(custom_list_of_dicts, input_content, file_content)
        messages = formatted_list_of_dicts
    else:
        formatted_prompt = custom_prompt.format(input_content=input_content, file_content=file_content)
        messages.append({"role": "user", "content": formatted_prompt})

if input_type == 'question' and not custom_prompt:
    messages.append({"role": "user", "content": input_content})
    
if input_type == 'question' and file_content and not custom_prompt:
    messages.append({"role": "user", "content": f"# {input_content}\n\n{file_content}"})

chat_log = []

if custom_data:
    construct_index(custom_data_path, custom_data_index_path)

while True:
  
    if custom_data:
        response_text = get_custom_data_response(messages[-1]["content"], custom_data_index_path)
    elif model == "gpt-4" or model == "gpt-3.5-turbo":
        response_text = get_chat_response(messages, model, openai, tokens)
    else:
        prompt = messages[-1]["content"]
        response_text = get_standard_response(prompt, model, openai, tokens)

    print(response_text)
    chat_log.append(response_text)

    if print_only or not continue_conversation():
        break

    messages.append({"role": "assistant", "content": response_text})
    user_input = input("Enter your next message (Press enter twice to finish):\n")
    multiline_input = []
    while user_input:
        multiline_input.append(user_input)
        user_input = input()
    user_input = "\n".join(multiline_input)
    messages.append({"role": "user", "content": user_input})
    chat_log.append(user_input)

if save_log:
    log_path = pathlib.Path(config.get('log_path', ''))
    log_path.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    log_file = log_path / f"{date_str}_{prompt_name}.log"
    with open(log_file, 'a') as file:
        for entry in chat_log:
            file.write(entry)
            file.write("\n")
    print(f"Chat log saved to {log_file}")
