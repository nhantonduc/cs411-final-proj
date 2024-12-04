import logging
import requests
import os
from notion_client import Client
from pprint import pprint
from dotenv import load_dotenv

from scholarship_finder.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

# Load environment variables from .env file
load_dotenv()

# Get your Notion Integration Token and Database ID from environment variables
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Initialize Notion client
notion = Client(auth=NOTION_API_KEY)

def fetch_scholarship_data():
    """
    Fetch scholarship data from the Notion database.
    Parses and returns the data in a dictionary format.
    """
    try:
        # Querying the Notion database
        query = notion.databases.query(database_id=DATABASE_ID)
        
        # Parsing results
        scholarships = []
        for result in query['results']:
            # Extracting the required properties
            scholarship = {
                "university": result['properties'].get('University', {}).get('rich_text', [{}])[0].get('text', {}).get('content', ''),
                "scholarship_name": result['properties'].get('Scholarship Name', {}).get('title', [{}])[0].get('text', {}).get('content', ''),
                "type": result['properties'].get('Type', {}).get('select', {}).get('name', ''),
                "degree_level": result['properties'].get('Degree Level', {}).get('select', {}).get('name', ''),
                "country": result['properties'].get('Country', {}).get('select', {}).get('name', ''),
                "deadline": result['properties'].get('Deadline', {}).get('date', {}).get('start', ''),
                "min_gpa": result['properties'].get('Min GPA', {}).get('number', None),
                "major": result['properties'].get('Major', {}).get('multi_select', [])
            }
            scholarships.append(scholarship)
        
        return scholarships
    
    except Exception as e:
        logger.error(f"Error fetching data from Notion: {str(e)}")
        return []

# Example usage
if __name__ == "__main__":
    data = fetch_scholarship_data()
    pprint(data)  # Prints the fetched scholarship data
