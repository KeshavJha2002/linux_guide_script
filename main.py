import json
import os
import configparser
import argparse
from tabulate import tabulate
from google.api_core.exceptions import InvalidArgument
import google.generativeai as genai

print("Author: https://github.com/KeshavJha2002")
# Define the configuration file path
CONFIG_FILE = 'config.ini'

# Load or create the configuration file
config = configparser.ConfigParser()

# If the configuration file exists, load it
if os.path.exists(CONFIG_FILE):
    config.read(CONFIG_FILE)

def parse_json(json_data, parser_function, query):
    try:
        data = json.loads(json_data)
        parser_function(data, query)
    except Exception as e:
        print(f"An error occurred while parsing JSON data: {e}")

def info_parser(data, query):
    try:
        command_data = data[query][0]
        table_data = []
        table_data.append(["Syntax", command_data["syntax"]])
        table_data.append(["Description", command_data["description"]])
        print(tabulate(table_data, tablefmt="fancy_grid"))

        # Adding options to the table
        table_data = []
        options = command_data["options"]
        for option, description in options.items():
            table_data.append([option, description])
        print(tabulate(table_data, headers=["Option", "Description"], tablefmt="grid"))

        # Adding examples to the table
        table_data = []
        for example in command_data["examples"]:
            table_data.append([example['command'], example['explanation']])

        print(tabulate(table_data, headers=["Example", "Explanation"], tablefmt="grid"))
    except KeyError:
        print("ERROR_MESSAGE")

def scenario_parser(data, query):
    try:
        # Access scenario
        scenario = data["scenario"]
        table_data = [["User Scenario", scenario]]
        print(tabulate(table_data, tablefmt="fancy_grid"))

        # Access commands
        table_data = []
        for command in data["commands"]:
            table_data.append([command['command'], command['description']])

        print(tabulate(table_data, headers=["Parameter", "Description"], tablefmt="grid"))
    except KeyError:
        print("ERROR_MESSAGE")

def get_api_key():
    """
    Prompt the user to enter the GenAI API key and write it to the configuration file.
    """
    api_key = input("Enter your GenAI API key: ")
    config['GENAI'] = {'api_key': api_key}

    # Write the API key to the configuration file
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def configure_genai():
    """
    Configure the GenAI API with the API key.
    """
    try:
        api_key = config['GENAI']['api_key']
        genai.configure(api_key=api_key)
    except KeyError:
        print("GenAI API key not found.")
        get_api_key()

def handle_api_key_error(error):
    """
    Handle API key errors.
    """
    if "API_KEY_INVALID" in str(error):
        print("InvalidArgument:", error)
        print("400 API key expired. Please renew the API key.")
        get_api_key()
    else:
        print("An error occurred:", error)

def main():
    """
    Main function to handle user inputs and generate responses.
    """
    parser = argparse.ArgumentParser(description="Command-line tool for GenAI")
    parser.add_argument(
        'query', 
        type=str, 
        nargs='?', 
        help="Enter the text"
    )
    parser.add_argument(
        '-i', '--info', 
        action='store_true', 
        help="Provide basic info and examples of the given command"
    )
    parser.add_argument(
        '-s', '--scenario', 
        action='store_true', 
        help="Suggest commands based on the user scenario"
    )

    args = parser.parse_args()

    configure_genai()

    if args.info:
        format_ = """
        json{
        "mkdir": [{
            "syntax": "mkdir [options] directory_name...",
            "description": "Creates one or more directories (folders). If the directory already exists, an error message will be printed.",
            "options": {
                "-p": "Creates any necessary parent directories.",
                "-v": "Prints the name of each directory created.",
                "-m mode": "Sets the permissions of the new directory to the specified mode.",
                "-Z context": "Sets the SELinux security context of the new directory to the specified value."
            },
            "examples": [
                {
                    "command": "mkdir mydir",
                    "explanation": "Creates a directory named 'mydir'."
                },
                {
                    "command": "mkdir -p mydir/sub1/sub2",
                    "explanation": "Creates a directory named 'mydir' and any necessary parent directories."
                },
                {
                    "command": "mkdir -m 755 mydir",
                    "explanation": "Creates a directory named 'mydir' with permissions set to 755."
                },
                {
                    "command": "mkdir -Z context=user_home_t mydir",
                    "explanation": "Creates a directory named 'mydir' with the specified SELinux security context."
                }
            ]
        }
        ]
        }
        """
        modified_prompt = f"{format_} strictly adhere to the given JSON format above and provide similar result to the command: '{args.query}' in JSON format. Don't include the 'mkdir' I sent in the response, use the command that is asked to you only."

        try:
            response = genai.GenerativeModel('gemini-1.5-flash').generate_content([modified_prompt]).text
            response = (response.replace("json", "").replace("JSON", "").lstrip("`").rstrip("`"))
            parse_json(response, info_parser, args.query)
        except InvalidArgument as e:
            handle_api_key_error(e)
    elif args.scenario:
        format_ = """
        json{
        "scenario": "I want to change the file write access to the admin only.",
        "commands": [
            {
                "description": "Using symbolic permissions",
                "command": "sudo chmod u=rw,go= /path/to/your/file"
            },
            {
                "description": "Using octal notation",
                "command": "sudo chmod 600 /path/to/your/file"
            },
            {
                "description": "Using symbolic permissions with shorthand",
                "command": "sudo chmod u+w /path/to/your/file && sudo chmod go= /path/to/your/file"
            },
            {
                "description": "Using symbolic permissions with absolute specification",
                "command": "sudo chmod u=rw,g=,o= /path/to/your/file"
            }
        ]
        }
        """
        modified_prompt = f"{format_} strictly adhere to the given JSON format above and provide Linux commands to accomplish the action described in the scenario: '{args.query}' in JSON format."

        try:
            response = genai.GenerativeModel('gemini-1.5-flash').generate_content([modified_prompt]).text
            response = (response.replace("json", "").replace("JSON", "").lstrip("`").rstrip("`"))
            parse_json(response, scenario_parser, args.query)
        except InvalidArgument as e:
            handle_api_key_error(e)
    else:
        print("Please select one of the two options: -i for command explainer or -s for scenario-based command suggestion.")

if __name__ == "__main__":
    main()
