import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
version = os.getenv('APP_VERSION')

data = {
    'version': version,
}

with open('version.json', 'w') as json_file:
    json.dump(data, json_file)
