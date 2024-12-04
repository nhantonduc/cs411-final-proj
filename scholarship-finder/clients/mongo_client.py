import logging
import os
from pymongo import MongoClient
from scholarship_finder.utils.logger import configure_logger

# Set up a logger for tracking application events and errors
logger = logging.getLogger(__name__)

# Configure the logger using a custom utility function
configure_logger(logger)

# Read MongoDB host and port from environment variables, or use default values if not set
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')  # Default host: localhost
MONGO_PORT = int(os.environ.get('MONGO_PORT', 27017))   # Default port: 27017

# Log a message indicating the connection attempt to MongoDB
logger.info("Connecting to MongoDB at %s:%d", MONGO_HOST, MONGO_PORT)

# Initialize a MongoDB client using the host and port
mongo_client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)

# Access the 'scholarship_finder' database
db = mongo_client['scholarship_finder']

# Access the 'sessions' collection within the database
sessions_collection = db['sessions']
