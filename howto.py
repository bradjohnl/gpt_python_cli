#!/usr/bin/env python3

import os
import openai
import sys

openai.api_key = os.environ.get('OPENAI_API_KEY')

# Take the request as a command line parameter and return the answer
request = sys.argv[1]

# Include command line argument flags to ask a generic question
if request == '--question' or request == '-q':
    question = sys.argv[2]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"""Q: {question}
A:""",
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " A:"]
    )
    print(response['choices'][0]['text'])
elif request == '--code' or request == '-c':
    code = sys.argv[2]
    response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=code,
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " A:"]
    )
    print(response['choices'][0]['text'])
else:
  print(openai.Completion.create(
    engine="text-davinci-003",
    prompt="Convert this text to a linux shell command.\n\nExample: Show all filesystems usage, space and mount point in human format\nOutput: df -h\n\nExample: Check the size of the pCloudDrive folder every 3 seconds\nOutput: while true; do du -sh pCloudDrive; sleep 1s; clear; done;\n\nExample: Find the smallest file in a directory and in all its subdirectories\nOutput: find . -type f -exec du -sh {} + | sort -n\nExample: "+request+"\nOutput:",
    temperature=0,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  ).choices[0].text)