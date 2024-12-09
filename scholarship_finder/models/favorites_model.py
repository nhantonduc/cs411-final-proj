import logging
from typing import List

# from scholarship_finder.models.scholarships_model import Scholarship
from scholarship_finder.utils.logger import configure_logger
from scholarship_finder.models.scholarship_model import Scholarship

# Done by Olu

logger = logging.getLogger(__name__)
configure_logger(logger)

class FavoritesModel:

    def __init__(self, user_id, favorites = None):
        self.user_id = user_id
        self.favorites = favorites or []
    
    def add_to_favorites(self, scholarship: 'Scholarship'):
        """
        Adds a scholarship to list of favorites.

        Args:
            scholarship (Scholarship): The scholarship object to be added to favorites
        """
        logger.info("Adding scholarship to favorites list...")
        scholarship_identifier = (scholarship.university, scholarship.scholarship_name)
        
        # Check if scholarship already exists by comparing university and name
        existing_identifiers = [(s.university, s.scholarship_name) for s in self.favorites]
        if scholarship_identifier not in existing_identifiers:
            self.favorites.append(scholarship)
            logger.info("Scholarship added successfully.")
        else:
            logger.error("Scholarship already exists in favorites list.")

    def remove_from_favorites(self, scholarship: 'Scholarship'):
        """
        Removes a scholarship from list of favorites.

        Args:
            scholarship (Scholarship): The scholarship object to be removed from favorites
        """
        logger.info("Removing scholarship from favorites list...")
        scholarship_identifier = (scholarship.university, scholarship.scholarship_name)
        
        # Find and remove scholarship by comparing university and name
        for saved_scholarship in self.favorites[:]:  # Create a copy to iterate
            if (saved_scholarship.university, saved_scholarship.scholarship_name) == scholarship_identifier:
                self.favorites.remove(saved_scholarship)
                logger.info("Scholarship removed successfully.")
                return
        logger.error("Scholarship not in favorites, cannot be removed.")

    def get_favorites(self) -> List['Scholarship']:
        """ Returns: All scholarships stored in the favorites list. """
        logger.info("Retrieving favorited scholarships...")
        return self.favorites

    def clear_favorites(self): 
        """ Removes all scholarships from the favorites list. """
        logger.info("Removing all favorited scholarships...")
        self.favorites = []
