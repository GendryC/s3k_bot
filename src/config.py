import os
from dotenv import load_dotenv

# @autor gendry
# @usage
# config = AppConfig()

class AppConfig:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
        load_dotenv(dotenv_path)
        self.config = {key: value for key, value in os.environ.items()}

    def get(self, key):
        return self.config.get(key, None)