import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# prerequisites
if 'TOKEN' not in os.environ:
    exit("No token provided")

BOT_TOKEN = os.environ['TOKEN']