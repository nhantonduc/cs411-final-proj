# Anya - Scholarship model class 
from dataclasses import asdict, dataclass
import datetime
from typing import List, Optional
from scholarship_finder.utils.logger import configure_logger

import logging

logger = logging.getLogger(__name__)
configure_logger(logger)


class Scholarship:
    """
    A class representing a scholarship with various attributes.

    Attributes:
        title (str): The title of the scholarship.
        description (str): A description of the scholarship.
        type (str): The type of scholarship (e.g., merit-based, need-based).
        country (str): The country where the scholarship is offered.
        requirements (List[str]): A list of requirements for the scholarship.
        deadline (datetime.date): The deadline for applying for the scholarship.
    """

    def __init__(
        self,
        title: str,
        description: str,
        type: str,
        country: str,
        requirements: List[str],
        deadline: datetime.date,
    ):
        self.title = title
        self.description = description
        self.type = type
        self.country = country
        self.requirements = requirements
        self.deadline = deadline

    @classmethod
    def filter_by_type(scholarships: List["Scholarship"], scholarship_type: str) -> List["Scholarship"]:
        """
        Filters scholarships by type.

        Args:
            scholarships (List[Scholarship]): The list of scholarships to filter.
            scholarship_type (str): The type to filter by.

        Returns:
            List[Scholarship]: A list of scholarships matching the specified type.
        """
        return [scholarship for scholarship in scholarships if scholarship.type == scholarship_type]

    @classmethod
    def filter_by_country(scholarships: List["Scholarship"], country: str) -> List["Scholarship"]:
        """
        Filters scholarships by country.

        Args:
            scholarships (List[Scholarship]): The list of scholarships to filter.
            country (str): The country to filter by.

        Returns:
            List[Scholarship]: A list of scholarships offered in the specified country.
        """
        return [scholarship for scholarship in scholarships if scholarship.country == country]

    @classmethod
    def filter_by_requirements(scholarships: List["Scholarship"], requirements: List[str]) -> List["Scholarship"]:
        """
        Filters scholarships by requirements.

        Args:
            scholarships (List[Scholarship]): The list of scholarships to filter.
            requirements (List[str]): A list of requirements to match.

        Returns:
            List[Scholarship]: A list of scholarships meeting all specified requirements.
        """
        return [
            scholarship
            for scholarship in scholarships
            if all(req in scholarship.requirements for req in requirements)
        ]

    @classmethod
    def sort_by_deadline(scholarships: List["Scholarship"]) -> List["Scholarship"]:
        """
        Sorts scholarships by deadline in ascending order.

        Args:
            scholarships (List[Scholarship]): The list of scholarships to sort.

        Returns:
            List[Scholarship]: A list of scholarships sorted by their deadlines.
        """
        return sorted(scholarships, key=lambda s: s.deadline)
