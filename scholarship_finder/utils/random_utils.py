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
        
        # Add debug logging
        logger.debug(f"Raw query response: {query}")
        
        scholarships = []
        for result in query.get('results', []):  # Use .get() with default empty list
            try:
                properties = result.get('properties', {})
                
                # More defensive property extraction
                rich_text = properties.get('University', {}).get('rich_text', [])
                university = rich_text[0].get('text', {}).get('content', '') if rich_text else ''
                
                title = properties.get('Scholarship Name', {}).get('title', [])
                scholarship_name = title[0].get('text', {}).get('content', '') if title else ''
                
                # For select fields, check if select is None before accessing name
                type_select = properties.get('Type', {}).get('select')
                type_name = type_select.get('name', '') if type_select else ''
                
                degree_select = properties.get('Degree Level', {}).get('select')
                degree_level = degree_select.get('name', '') if degree_select else ''
                
                country_select = properties.get('Country', {}).get('select')
                country = country_select.get('name', '') if country_select else ''
                
                date = properties.get('Deadline', {}).get('date')
                deadline = date.get('start', '') if date else ''
                
                scholarship = {
                    "university": university,
                    "scholarship_name": scholarship_name,
                    "type": type_name,
                    "degree_level": degree_level,
                    "country": country,
                    "deadline": deadline,
                    "min_gpa": properties.get('Min GPA', {}).get('number'),
                    "major": properties.get('Major', {}).get('multi_select', [])
                }
                scholarships.append(scholarship)
            except Exception as e:
                logger.error(f"Error processing individual scholarship: {str(e)}")
                continue
        
        return scholarships
    
    except Exception as e:
        logger.error(f"Error fetching data from Notion: {str(e)}")
        return []

# Example usage
if __name__ == "__main__":
    data = fetch_scholarship_data()
    pprint(data)  # Prints the fetched scholarship data
