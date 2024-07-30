import argparse
from genai_client import GenAIClient
from command_parser import InfoParser, ScenarioParser
from prompt_sample import info_format_, scenario_format_

def main():
    parser = argparse.ArgumentParser(description="Command-line tool for GenAI")
    parser.add_argument('query', type=str, nargs='?', help="Enter the text")
    parser.add_argument('-i', '--info', action='store_true', help="Provide basic info and examples of the given command")
    parser.add_argument('-s', '--scenario', action='store_true', help="Suggest commands based on the user scenario")

    args = parser.parse_args()
    client = GenAIClient()

    if args.info:
        prompt = f"{info_format_} strictly adhere to the given JSON format above and provide similar result to the command: '{args.query}' in JSON format. Don't include the 'mkdir' I sent in the response, use the command that is asked to you only."
        response = client.generate_content(prompt)
        parser = InfoParser()
        parser.parse_json(response, args.query)

    elif args.scenario:
        prompt = f"{scenario_format_} strictly adhere to the given JSON format above and provide Linux commands to accomplish the action described in the scenario: '{args.query}' in JSON format."
        response = client.generate_content(prompt)
        parser = ScenarioParser()
        parser.parse_json(response, args.query)
    else:
        print("Please select one of the two options: -i for command explainer or -s for scenario-based command suggestion.")

if __name__ == "__main__":
    main()
