import os
import logging
import pymongo

MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")

client = None

if MONGO_URI:
    try:
        # Check if the URI is already URL-encoded or needs it. 
        # The provided URI in local.settings.json seems to be already encoded for username/password.
        client = pymongo.MongoClient(MONGO_URI)
        logging.info("MongoDB client initialized.")
    except Exception as e:
        logging.error(f"Failed to initialize MongoDB client: {e}")
else:
    logging.warning("MONGO_URI not found in environment variables.")
