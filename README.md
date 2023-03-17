# GPT Python CLI

## DISCLAIMER:

This project, GPT_Python_CLI, is an independently developed tool and is not affiliated with, endorsed, or supported by OpenAI Inc. It is not an official client for the OpenAI API, nor is it developed or maintained by OpenAI.

The GPT_Python_CLI project aims to provide a convenient command-line interface for users to interact with GPT-4 language models through the OpenAI API. Any opinions, findings, conclusions, or recommendations expressed in this project are those of the author(s) and do not necessarily reflect the views of OpenAI Inc.

Please refer to OpenAI's official documentation for the most accurate and up-to-date information regarding the OpenAI API, GPT models, and their usage.

## Introduction

A Python-based command-line interface (CLI) for interacting with OpenAI's GPT-4 model. With this CLI, you can ask questions, generate text, and use custom prompts to control the model's output.

## Features

- Query GPT-4 with generic questions
- Generate code using GPT-4
- Use custom prompts from a library. Create and edit your prompts and share them with others!
- Save chat logs to a specified path
- Interactive chat mode or one-shot mode
- Customize model options like temperature and token limits (COMING SOON)
- Syntax highlighting for code output (COMING SOON)
- Save valid prompts for future model training (COMING SOON)
- Online portal for sharing custom prompts (COMING SOON)

## Installation

1. Clone the repository:

  ```bash
  git clone https://github.com/bradjohnl/gpt_python_cli.git
  ```

1. Navigate to the repository directory:

```bash
cd gpt_python_cli
```

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

1. Set up an OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

1. Create a configuration file in your home directory:

```bash
mkdir ~/.gpt_python_cli
cp config_sample.json ~/.gpt_python_cli/config.json
```

1. Customize the paths in config.json

## Usage

```bash
./openai_cli.py [options]

Options:

    --question, -q <question>: Ask a generic question
    --model, -m <model>: Specify the model to use (gpt-4 only for the moment)
    --file, -f <file_path>: Use a file as input for the model
    --prompt, -p <prompt_name>: Use a custom prompt from the library
    --print-only, -po: Print the command without asking to continue
    --save-log, -sl: Save the chat log to a default path
    --help, -h: Show the help message

```

## Configuration File

Create a JSON configuration file at ~/.gpt_python_cli/config.json with the following content:

```json
{
  "library_path": "/path/to/your/custom/prompts/directory",
  "log_path": "/path/to/your/chat/logs/directory"
}
```

Replace `/path/to/your/custom/prompts/directory` and `/path/to/your/chat/logs/directory` with the paths to your custom prompts and chat logs directories, respectively.

## Custom Prompts

Custom prompts are text files containing a prompt template that you can use with the CLI. You can use placeholders like {input_content} and {file_content} to represent the user's input and the content of a file, respectively.

Create a text file inside your custom prompts directory with the same name as your custom prompt and a .txt extension. Write your custom prompt template, and use double curly brackets to include JSON syntax. For example:

```json
{{"role": "system", "content": "You are a helpful assistant."}},
{{"role": "user", "content": "Convert the following text to a Linux shell command. Just print the command without any other output: {input_content}"}}
```

To use a custom prompt with the CLI, run:

```bash
./openai_cli.py --prompt custom_prompt_name --file input.txt
```

Replace custom_prompt_name with the name of your custom prompt (without the extension).

You can also use simpler prompts such as:
Don't forget to include placeholders for the user's input and file content! ({input_content} and {file_content}, respectively)}


## Examples

### Ask a generic question and enter interactive chat mode

```bash:

```bash
./openai_cli.py --question "What is the capital of France?"
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
from openai_cli import print_help, continue_conversation, load_config, load_prompt

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

### Use a custom prompt from the library

In this example, we have added a custom prompt file named find_command.txt to the library directory. The prompt template is:

```json
{{"role": "system", "content": "You are a helpful assistant."}},
{{"role": "user", "content": "Convert the following text to a Linux shell command. Just print the command without any other output: {input_content}"}}
```

Run the following command to use the custom prompt:

```bash
./gpt_python_cli.py --prompt find_command --print-only -q "Find all files in the current directory that contain the word 'test'"
```

#### Output

```bash
grep -lir "test" .
```

#### Additional explanation

Furthermore, we have added the `--print-only` flag to only print the output of the command, without the prompt that allows us to continue the conversation.

### Save the chat log to a default path:

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
Chat log saved to /home/keepupdragon/.openai_cli/logs/20230317_None.log
```

#### Additional explanation

You may notice that the log file name is `20230317_None.log`. This is because there is no custom prompt name specified, so the prompt name is set to `None`. The log file name is generated using the current date and time, and the prompt name.

## Contributing

Contributions are welcome! If you'd like to help improve this project, please submit a pull request with your changes or create an issue to discuss your ideas.

### Public prompts

If you'd like to share your custom prompt with the community, please submit a pull request to add it to the `prompts` directory.

If you are using a JSON prompt, please make sure that the prompt is valid JSON. You can use a tool like [JSONLint](https://jsonlint.com/) to validate your JSON. You will still need to save it as a `.txt` file.

Make sure you are using at least one placeholder in your prompt. The placeholder will be replaced with the user's input.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0). See the [LICENSE.md](LICENSE.md) file for more details.

