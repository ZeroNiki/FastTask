from dotenv import load_dotenv
import os


# Main env
load_dotenv(".env")

# Dev env
load_dotenv(".dev_env")

TOKEN = str(os.getenv("TOKEN"))
FASTAPI_URL = str(os.getenv("FASTAPI_URL"))
