import os
import configparser

CONFIG_FILE = '/mnt/c/Users/jhak7/Desktop/Friendly_CLI/config.ini'

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self._load_config()

    def _load_config(self):
        if os.path.exists(CONFIG_FILE):
            self.config.read(CONFIG_FILE)

    def get_api_key(self):
        try:
            return self.config['GENAI']['api_key']
        except KeyError:
            return None

    def set_api_key(self, api_key):
        self.config['GENAI'] = {'api_key': api_key}
        with open(CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)
