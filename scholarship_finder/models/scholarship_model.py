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
    A class representing a scholarship with various attributes matching Notion database structure.
    """

    def __init__(
        self,
        university: str,
        scholarship_name: str,
        type: str,
        degree_level: str,
        country: str,
        deadline: str,
        min_gpa: float = None,
        major: list = None
    ):
        self.university = university
        self.scholarship_name = scholarship_name
        self.type = type
        self.degree_level = degree_level
        self.country = country
        self.deadline = deadline
        self.min_gpa = min_gpa
        self.major = major if major else []

    @classmethod
    def filter_by_type(cls, scholarships: List["Scholarship"], scholarship_type: str) -> List["Scholarship"]:
        """Filters scholarships by type."""
        return [s for s in scholarships if s.type == scholarship_type]

    @classmethod
    def filter_by_country(cls, scholarships: List["Scholarship"], country: str) -> List["Scholarship"]:
        """Filters scholarships by country."""
        return [s for s in scholarships if s.country == country]

    @classmethod
    def filter_by_degree_level(cls, scholarships: List["Scholarship"], degree_level: str) -> List["Scholarship"]:
        """Filters scholarships by degree level."""
        return [s for s in scholarships if s.degree_level == degree_level]

    @classmethod
    def filter_by_min_gpa(cls, scholarships: List["Scholarship"], min_gpa: float) -> List["Scholarship"]:
        """Filters scholarships by minimum GPA requirement."""
        return [s for s in scholarships if s.min_gpa and s.min_gpa <= min_gpa]

    @classmethod
    def sort_by_deadline(cls, scholarships: List["Scholarship"]) -> List["Scholarship"]:
        """Sorts scholarships by deadline."""
        return sorted(scholarships, key=lambda s: s.deadline)