import logging
from typing import List

# from scholarship_finder.models.scholarships_model import Scholarship
from scholarship_finder.utils.logger import configure_logger

# Done by Olu

logger = logging.getLogger(__name__)
configure_logger(logger)

class FavoritesModel:

    def __init__(self, user_id, favorites = None):
        self.user_id = user_id
        self.favorites = favorites or []
    
    def add_to_favorites(self, scholarship_id):
        """
        Adds a scholarship to list of favorites using the scholarship's ID.

        Args:
            scholarship_id (int): the ID of scholarship being added to favorites
        """
        logger.info("Adding scholarship to favorites list...")
        if scholarship_id not in self.favorites:
            self.favorites.append(scholarship_id)
            logger.info("Scholarship added successfully.")
        else:
            logger.error("Scholarship already exists in favorites list.")

    def remove_from_favorites(self, scholarship_id):
        """
        Removes a scholarship from list of favorites using the scholarship's ID.

        Args:
            scholarship_id (int): the ID of scholarship being added to favorites
        """
        logger.info("Removing scholarship from favorites list...")
        if scholarship_id in self.favorites:
            self.favorites.remove(scholarship_id)
            logger.info("Scholarship removed successfully.")
        else:
            logger.error("Scholarship not in favorites, cannot be removed.")

    def get_favorites(self): #"""-> List[Scholarship]"""
        """ Returns: All scholarships stored in the favorites list. """
        logger.info("Retrieving favorited scholarships...")
        return self.favorites

    def clear_favorites(self): 
        """ Removes all scholarships from the favorites list. """
        logger.info("Removing all favorited scholarships...")
        self.favorites = []
