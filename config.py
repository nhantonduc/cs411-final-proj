import os

class ProductionConfig():
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # This would almost universally be false in a Flask app
                                           # But we are doing unnecessarily complicated Redis
                                           # write-throughs
    SQLALCHEMY_DATABASE_URI = 'sqlite:///scholarship_finder.db'  # or your preferred database URI
    NOTION_DATABASE_ID = "157b2df7f84a81e98082febf3604e719"  # Replace with your actual Notion database ID
    
class TestConfig():
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database for tests
