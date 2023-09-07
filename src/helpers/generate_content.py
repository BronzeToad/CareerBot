import openai
from dotenv import load_dotenv
import os


# =========================================================================== #

def get_openai_api_key():
    """Retrieve the OpenAI API key from the .env file."""

    load_dotenv()
    api_key = os.getenv("openai_api_key")

    if api_key is None:
        raise Exception("OpenAI API key not found in .env file.")

    return api_key


