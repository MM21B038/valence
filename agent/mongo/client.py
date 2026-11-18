import os
from urllib.parse import quote_plus
from pymongo import MongoClient

MONGO_USER = quote_plus(os.environ["MONGO_USER"])
MONGO_PASSWORD = quote_plus(os.environ["MONGO_PASSWORD"])
MONGO_PORT = os.getenv("MONGO_PORT", "27017")

MONGO_URI = (
    f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}"
    f"@valence_mongo:{MONGO_PORT}/?authSource=admin"
)

def get_chat_sessions_collection():
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000,
    )

    db = client["valence"]
    return db["chat_sessions"]


