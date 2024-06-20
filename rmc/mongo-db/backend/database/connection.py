import os
from pymongo import MongoClient
from dotenv import load_dotenv  #pip install python-dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URL"))
#db = client.get_database(os.getenv("MONGO_DATABASE"))
db = client[os.getenv("MONGO_DATABASE")]


