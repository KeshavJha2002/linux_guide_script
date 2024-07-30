import json
from tabulate import tabulate

class CommandParser:
    def parse_json(self, json_data, query):
        try:
            data = json.loads(json_data)
            self.parse(data, query)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")

class InfoParser(CommandParser):
    def parse(self, data, query):
        command_data = data.get(query, [{}])[0]
        self.display_command_info(command_data)

    def display_command_info(self, command_data):
        table_data = [["Syntax", command_data.get("syntax", "N/A")],
                      ["Description", command_data.get("description", "N/A")]]
        print(tabulate(table_data, tablefmt="fancy_grid"))

        options = command_data.get("options", {})
        if options:
            table_data = [[opt, desc] for opt, desc in options.items()]
            print(tabulate(table_data, headers=["Option", "Description"], tablefmt="grid"))

        examples = command_data.get("examples", [])
        if examples:
            table_data = [[ex["command"], ex["explanation"]] for ex in examples]
            print(tabulate(table_data, headers=["Example", "Explanation"], tablefmt="grid"))

class ScenarioParser(CommandParser):
    def parse(self, data, query):
        scenario = data.get("scenario", "N/A")
        print(tabulate([["User Scenario", scenario]], tablefmt="fancy_grid"))

        commands = data.get("commands", [])
        if commands:
            table_data = [[cmd["command"], cmd["description"]] for cmd in commands]
            print(tabulate(table_data, headers=["Command", "Description"], tablefmt="grid"))
