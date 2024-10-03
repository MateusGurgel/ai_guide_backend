#type: ignore

from openai import OpenAI
from decouple import config

OPENAI_API_KEY = str(config("OPENAI_API_KEY", default=""))
openai_client = OpenAI(api_key=OPENAI_API_KEY)