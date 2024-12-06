from dotenv import load_dotenv
import os

# Dev env
load_dotenv(".dev_env")

# Main env
load_dotenv(".env")

TOKEN = str(os.getenv("TOKEN"))
FASTAPI_URL = str(os.getenv("FASTAPI_URL"))
