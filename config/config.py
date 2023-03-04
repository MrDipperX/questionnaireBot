import os
from os.path import join, dirname
from dotenv import load_dotenv
import json

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN")
GROUP_ID = os.environ.get("GROUP_ID")

HOST = os.environ.get("HOST")
DBNAME = os.environ.get("DBNAME")
USER = os.environ.get("USER")
PORT = os.environ.get("PORT")
PASSWORD = os.environ.get("PASSWORD")

with open("utils/phrases.json", "r", encoding="utf-8") as lang_file:
    phrases = json.load(lang_file)

