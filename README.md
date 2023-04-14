# GPT Python CLI

## DISCLAIMER:

This project, GPT_Python_CLI, is an independently developed tool and is not affiliated with, endorsed, or supported by OpenAI Inc. It is not an official client for the OpenAI API, nor is it developed or maintained by OpenAI.

It also allows you to use the gpt_index Python library to index your custom data and use it with the ChatGPT API. This is a great way to train your own custom AI chatbot using the ChatGPT API. You can find more information about the gpt_index (LLama index) library here: https://gpt-index.readthedocs.io/en/latest/index.html

The GPT_Python_CLI project aims to provide a convenient command-line interface for users to interact with language models through the OpenAI API. Any opinions, findings, conclusions, or recommendations expressed in this project are those of the author(s) and do not necessarily reflect the views of OpenAI Inc.

Please refer to OpenAI's official documentation for the most accurate and up-to-date information regarding the OpenAI API, GPT models, and their usage.

## Introduction

An unofficial Python-based command-line interface (CLI) for interacting with OpenAI's GPT-4 model. With this CLI, you can ask questions, generate text, and use custom prompts to control the model's output.

## Features

- Query GPT-4 with generic questions
- Generate code using GPT-4
- Use custom prompts from a library. Create and edit your prompts and share them with others!
- Save chat logs to a specified path
- Interactive chat mode or one-shot mode
- Customize model options like temperature and token limits
- Syntax highlighting for code output (COMING SOON?)
- Save valid prompts for future model training (COMING SOON?)
- Online portal for sharing custom prompts (COMING SOON?)
- Run ChatGPT against custom data (Thanks to https://beebom.com/how-train-ai-chatbot-custom-knowledge-base-chatgpt-api/)

## Installation

1. Clone the repository:

  ```bash
  git clone https://github.com/bradjohnl/gpt_python_cli.git
  ```

2. Navigate to the repository directory:

```bash
cd gpt_python_cli
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Set up an OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

5. Create a configuration file in your home directory:

```bash
mkdir ~/.gpt_python_cli
cp config_sample.json ~/.gpt_python_cli/config.json
```

6. Customize the paths in config.json

## Usage

```bash
./gpt_python_cli.py [options]

Options:

  --question, -q <question>         Ask a generic question
  --model, -m <model>               Specify the model to use (gpt-4 only for the moment)
  --file, -f <file_path>            Use a file as input for the model
  --prompt, -p <prompt_name>        Use a custom prompt from the library
  --print-only, -po                 Print the command without asking to continue
  --save-log, -sl                   Save the chat log to a default path
  --tokens, -t <tokens>             Specify the number of tokens to use (default: 2000)
  --add-to-index, -ai <file_path>   Add a file to the custom index
  --index-path, -ip <index_path>    Specify the directory path where the custom index is located be used with custom data
  --help, -h                        Show this help message

```

## Configuration File

Create a JSON configuration file at ~/.gpt_python_cli/config.json with the following content:

```json
{
  "library_path": "/home/user/.gpt_python_cli/library",
  "log_path": "/home/user/.gpt_python_cli/logs",
  "models": {
    "gpt-4": "gpt-4",
    "text": "text-davinci-003",
    "code": "code-davinci-002"
  }
}
```

Replace the values with the paths to your custom prompts and chat logs directories, respectively. You can also customize the model names to use for each model type.

## Custom Prompts

Custom prompts are text and JSON files containing a prompt template that you can use with the CLI. You can use placeholders like {input_content} and {file_content} to represent the user's input and the content of a file, respectively.

See below for some examples.

## Examples

### Ask a generic question and enter interactive chat mode

```bash
./gpt_python_cli.py --question "What is the capital of France?"
```

#### Output:
```bash
The capital of France is Paris.
Do you want to continue the conversation? (y/n): y
Enter your next message (Press enter twice to finish):
What are the must see spots of Paris?

There are numerous must-see spots in Paris, including:

1. Eiffel Tower: This iconic landmark is a symbol of Paris and offers stunning views of the city from its observation decks.

2. Louvre Museum: Home to the famous Mona Lisa painting, the Louvre is one of the largest and most renowned art museums in the world.

3. Notre-Dame Cathedral: This Gothic masterpiece is known for its detailed architecture, beautiful stained glass windows, and historical significance.

4. Champs-Élysées: This famous avenue is lined with shops, restaurants, and theaters, and it leads up to the Arc de Triomphe.

5. Montmartre: A charming neighborhood known for its bohemian atmosphere, artists, and the Sacré-Cœur Basilica.

6. Palace of Versailles: A royal château just outside of Paris, this historical site is recognized for its breathtaking gardens, opulent palace, and the Hall of Mirrors.

7. Musée d'Orsay: An impressive museum housed in a former train station, the Musée d'Orsay features works by famous artists such as Monet, Van Gogh, and Renoir.

8. Sainte-Chapelle: A stunning Gothic chapel known for its incredible stained glass windows.

9. Seine River Cruise: A scenic boat tour along the Seine River that offers a unique perspective of Paris' monuments and architecture.

10. The Latin Quarter: A historic district filled with narrow streets, charming cafes, and the Panthéon, where many famous French figures are buried.

These are just a few examples of the many attractions that make Paris a beloved destination for travelers from all over the world.
```

### Generate code using GPT-4:

```bash
./gpt_python_cli.py --file gpt_python_cli.py --question "Generate unit tests for the following code:"
```

#### Output:

```python
import unittest
import os
import json
import tempfile
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from gpt_python_cli import print_help, continue_conversation, load_config, load_prompt

class TestOpenAICLI(unittest.TestCase):

    def test_print_help(self):
        with patch("builtins.print") as mock_print:
            print_help()
            mock_print.assert_called()

    @patch("builtins.input", side_effect=["y"])
    def test_continue_conversation_yes(self, mock_input):
        result = continue_conversation()
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["n"])
    def test_continue_conversation_no(self, mock_input):
        result = continue_conversation()
        self.assertFalse(result)

    @patch("builtins.open")
    def test_load_config(self, mock_open):
        example_config = {"config_key": "config_value"}
        file_mock = MagicMock()
        file_mock.__enter__ = MagicMock(return_value=file_mock)
        file_mock.__exit__ = MagicMock(return_value=None)
        file_mock.read = MagicMock(return_value=json.dumps(example_config))
        mock_open.return_value = file_mock
        
        config = load_config()
        self.assertEqual(config, example_config)

    def test_load_prompt(self):
        prompt_content = "Example prompt"
        temporary_file = tempfile.NamedTemporaryFile(delete=False)
        temporary_file.write(prompt_content.encode())
        temporary_file.close()
        
        base_path, prompt_filename = os.path.split(temporary_file.name)
        prompt_name = os.path.splitext(prompt_filename)[0]
        
        loaded_prompt = load_prompt(prompt_name, base_path)
        self.assertEqual(loaded_prompt, prompt_content)
        
        os.unlink(temporary_file.name)

if __name__ == '__main__':
    unittest.main()
```

### Use other models

In this example, we use the text model from our config example (text-davinci-003).

```bash
./gpt_python_cli.py --model text --question "What is the capital of France?"
```

#### Output:

```bash
Paris.
Do you want to continue the conversation? (y/n): n
```

### Use custom data from a file

We have the bitcoin whitepaper in the library directory. 
Now we can ask questions about the document in the following way:

```bash
cd btc_whitepaper
./gpt_python_cli.py --ai btc_whitepaper.pdf
./gpt_python_cli.py --ip .index.json --question "What is the double-spending problem?"
```

```bash
This document is about a proposed solution to the double-spending problem using a peer-to-peer network. It explains how digital signatures can provide part of the solution, and how the network can timestamp transactions by hashing them into an ongoing chain of hash-based proof-of-work. It also discusses how the longest chain serves as proof of the sequence of events witnessed, and how the network requires minimal structure.
Do you want to continue the conversation? (y/n): n

```

### Add multiple files to the index and use them in the conversation

Let's add all the files in the current repository to the index:
```bash
cd gpt_python_cli
for i in $(ls); do ./gpt_python_cli.py -ai $i; done; 
./gpt_python_cli.py --ip . --question "What is this repo about?"
```

#### Output:

```bash
Loaded index from disk
INFO:gpt_index.token_counter.token_counter:> [query] Total LLM token usage: 87 tokens
INFO:gpt_index.token_counter.token_counter:> [query] Total embedding token usage: 6 tokens

This repo appears to be about using Python libraries such as openai, pathlib, datetime, PyPDF2, and gpt_index to create and manipulate data.
Do you want to continue the conversation? (y/n): y
Enter your next message (Press enter twice to finish):
What is the license used? Am I allowed it to use this code for commercial purposes?

INFO:gpt_index.token_counter.token_counter:> [query] Total LLM token usage: 564 tokens
INFO:gpt_index.token_counter.token_counter:> [query] Total embedding token usage: 18 tokens

The license used is Creative Commons Attribution-NonCommercial 4.0 International. You are not allowed to use this code for commercial purposes.
```

### Add multiple files recursing into subfolders to the same index and use them in the conversation

In this example, we want to ask questions about the Auto-GPT repo: https://github.com/Torantulino/Auto-GPT


```bash
find . -type f -not -path '*/\.*' -exec gpt_python_cli.py -ip .index.json -ai {} \;
gpt_python_cli.py -ip . -q "What's the azure.yaml.template file for?"
```

**Output:**

```bash
Loaded index from disk
INFO:gpt_index.token_counter.token_counter:> [query] Total LLM token usage: 245 tokens
INFO:gpt_index.token_counter.token_counter:> [query] Total embedding token usage: 14 tokens
The azure.yaml.template file is used to configure the Azure API for use with the specified models. It contains the API type, base URL, version, and model deployment IDs for the fast_llm_model, smart_llm_model, and embedding_model.
```

Now let's ask a question about a file in a subfolder:
```bash 
gpt_python_cli.py -ip . -q "What's the ai_config.py file for?"
```

**Output**

```text
The ai_config.py file is a class object that contains the configuration information for the AI. It is used to store the AI's name, role, and goals, and can be used to generate a prompt for the user. It also has methods to save and load the configuration information from a yaml file.
Do you want to continue the conversation? (y/n):
```

### Use a custom prompt from the library

#### JSON prompt
In this example, we have added a custom prompt file named `pirate.json` to the library directory. The prompt template is:

```json
[
	{
		"role": "system", 
		"content": "You are a pirate. You will act and reply as if you are one of the most feared pirates across all seas and oceans."	
	},
	{
		"role": "user", 
		"content": "{input_content}"
	}
]
```

Run the following command to use the custom prompt:

```bash
./gpt_python_cli.py -p pirate -q "How do I find the most precious treasure of all times?"
```

##### Output

```
Ahoy there, me hearty! If ye be lookin' for the most precious treasure of all times, ye must be prepared to face great danger and challenges. The first step is to gather a crew of loyal and skilled pirates who are willing to follow ye to the ends of the earth. 

Next, ye must acquire a map or clues that lead to the location of the treasure. This may involve negotiating with other pirates, stealing from wealthy merchants, or even battling sea monsters. 

Once ye have the map or clues, ye must set sail and navigate through treacherous waters and unpredictable weather. Be prepared to face storms, reefs, and other obstacles that may stand in yer way. 

When ye finally reach the location of the treasure, ye must be ready to defend it from other pirates who may also be seeking it. This may involve engaging in a fierce battle or using cunning tactics to outsmart yer opponents. 

Remember, the most precious treasure of all times is not just gold and jewels, but also the thrill of the adventure and the camaraderie of yer crew. So set sail, me hearty, and may the winds be in yer favor!

```

#### Text prompt

In this example, we have added a custom prompt file named `find_command.txt` to the library directory. The prompt template is:

```txt
Convert the following text to a linux shell command. Just print the command without any other output: {input_content}
```

Run the following command to use the custom prompt:

```bash
./gpt_python_cli.py -p find_command -q "Find a random number between 1 and 10"
```

##### Output

```bash
echo $((RANDOM % 10 + 1))
Do you want to continue the conversation? (y/n):
```

#### Additional explanation

Furthermore, we have added the `--print-only` flag to only print the output of the command, without the prompt that allows us to continue the conversation.

### Save the chat log to a default path

```bash
./gpt_python_cli.py --save-log --question "What is the purpose of a transformer in an electrical system?"
```

#### Output:
```
A transformer is a crucial component in an electrical system, serving several purposes, including:

1. Voltage regulation: Transformers are used to step up or step down the voltage levels between different parts of an electrical system. For example, they may increase the voltage coming from power plants for long-distance transmission and decrease it for local distribution to consumers.

2. Isolation: Transformers provide electrical isolation between two circuits, which helps in maintaining safety, reducing noise, and preventing electrical faults.

3. Impedance matching: In some applications like audio systems, transformers help match the impedance of different devices or components to ensure the maximum transfer of power and minimize signal loss.

4. Current control: Transformers can be used to limit or control the current flowing in a circuit, thereby providing protection against overloads and short circuits.

5. Phase shifting: In certain power system applications, transformers are employed to control the phase angle between voltage and current, which aids in power flow management and system stability.
Do you want to continue the conversation? (y/n): n
Chat log saved to /home/test/.gpt_python_cli/logs/20230317_None.log
```

#### Additional explanation

You may notice that the log file name is `20230317_None.log`. This is because there is no custom prompt name specified, so the prompt name is set to `None`. The log file name is generated using the current date and time, and the prompt name.

## Contributing

Contributions are welcome! If you'd like to help improve this project, please submit a pull request with your changes or create an issue to discuss your ideas.

## Known issues:
- [ ] JSON data needs to be split into approx. 1MB chunks otherwise the error: `AssertionError: The batch size should not be larger than 2048.` will occur. There is an open bug on gpt_index tracking this issue: https://github.com/jerryjliu/gpt_index/issues/517

## TODOs:

- [ ] Add support for other models (e.g. image, audio, etc.)
- [ ] Add support for custom prompt on custom data.
- [ ] Add pre-commit config
- [ ] Add Pr templates.
- [ ] Add issue templates.
- [ ] Add contributing guidelines.
- [ ] Add Docker support.
- [ ] Colorized output to distinguish questions and answers.
- [ ] Syntax highlighting for code snippets.
- [ ] Fetch custom data from websites.

### Public prompts

If you'd like to share your custom prompt with the community, please submit a pull request to add it to the `prompts` directory.

If you are using a JSON prompt, please make sure that the prompt is valid JSON. You can use a tool like [JSONLint](https://jsonlint.com/) to validate your JSON.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0). See the [LICENSE.md](LICENSE.md) file for more details.

