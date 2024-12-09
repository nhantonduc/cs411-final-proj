import os

class ProductionConfig():
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # This would almost universally be false in a Flask app
                                           # But we are doing unnecessarily complicated Redis
                                           # write-throughs
    SQLALCHEMY_DATABASE_URI = 'sqlite:///scholarship_finder.db'  # or your preferred database URI
    NOTION_DATABASE_ID = "1496ed96f61f80cf8f32c1b591a2c6be"  # Replace with your actual Notion database ID
    
class TestConfig():
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database for tests