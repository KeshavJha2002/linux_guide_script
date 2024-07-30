from google.api_core.exceptions import InvalidArgument
import google.generativeai as genai
from config import Config

class GenAIClient:
    def __init__(self):
        self.config = Config()
        self._configure_genai()

    def _configure_genai(self):
        api_key = self.config.get_api_key()
        if api_key:
            genai.configure(api_key=api_key)
        else:
            raise InvalidArgument("API key is missing. Please set the API key.")

    def generate_content(self, prompt):
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt])
        return response.text
