#!/usr/bin/env python3

import os
import openai
import sys

openai.api_key = os.environ.get('OPENAI_API_KEY')

# Take the request as a command line parameter and return the answer
request = sys.argv[1]


print(openai.Completion.create(
  engine="code-davinci-002",
  prompt=request,
  temperature=0,
  max_tokens=500,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
).choices[0].text)
