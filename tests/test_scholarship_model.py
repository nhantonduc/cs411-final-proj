import pytest
import datetime

from scholarship_finder.models.scholarship_model import Scholarship

@pytest.fixture
def scholarship_1():
    return Scholarship(
        university="MIT",
        scholarship_name="Merit Scholarship",
        type="Merit-based",
        degree_level="Undergraduate",
        country="USA",
        deadline="2024-01-15",
        min_gpa=3.5,
        major=["Computer Science", "Engineering"]
    )

@pytest.fixture
def scholarship_2():
    return Scholarship(
        university="Stanford",
        scholarship_name="Need Scholarship",
        type="Need-based",
        degree_level="Graduate",
        country="USA",
        deadline="2024-02-20",
        min_gpa=3.0,
        major=["Any"]
    )

@pytest.fixture
def scholarship_3():
    return Scholarship(
        university="University of Toronto",
        scholarship_name="STEM Scholarship",
        type="Merit-based",
        degree_level="Undergraduate",
        country="Canada",
        deadline="2024-03-10",
        min_gpa=3.7,
        major=["STEM"]
    )

@pytest.fixture
def scholarship_list(scholarship_1, scholarship_2, scholarship_3):
    return [scholarship_1, scholarship_2, scholarship_3]

def test_filter_by_type(scholarship_list):
    """Test filtering scholarships by type."""
    merit_scholarships = Scholarship.filter_by_type(scholarship_list, "Merit-based")
    assert len(merit_scholarships) == 2
    assert all(s.type == "Merit-based" for s in merit_scholarships)

def test_filter_by_country(scholarship_list):
    """Test filtering scholarships by country."""
    usa_scholarships = Scholarship.filter_by_country(scholarship_list, "USA")
    assert len(usa_scholarships) == 2
    assert all(s.country == "USA" for s in usa_scholarships)

def test_sort_by_deadline(scholarship_list):
    """Test sorting scholarships by deadline."""
    sorted_scholarships = Scholarship.sort_by_deadline(scholarship_list)
    deadlines = [s.deadline for s in sorted_scholarships]
    assert deadlines == sorted(deadlines)

def test_filter_by_degree_level(scholarship_list):
    """Test filtering scholarships by degree level."""
    undergrad_scholarships = Scholarship.filter_by_degree_level(scholarship_list, "Undergraduate")
    assert len(undergrad_scholarships) == 2
    assert all(s.degree_level == "Undergraduate" for s in undergrad_scholarships)

def test_filter_by_min_gpa(scholarship_list):
    """Test filtering scholarships by minimum GPA."""
    qualified_scholarships = Scholarship.filter_by_min_gpa(scholarship_list, 3.6)
    assert len(qualified_scholarships) == 2