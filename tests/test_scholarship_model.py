import pytest
import datetime

from scholarship_finder.models.scholarship_model import Scholarship

@pytest.fixture
def scholarship_1():
    return Scholarship(
        title="Merit Scholarship",
        description="Awarded for academic excellence.",
        type="Merit-based",
        country="USA",
        requirements=["GPA > 3.5"],
        deadline=datetime.date(2024, 1, 15),
    )

@pytest.fixture
def scholarship_2():
    return Scholarship(
        title="Need Scholarship",
        description="Awarded for financial need.",
        type="Need-based",
        country="USA",
        requirements=["Income < 50000"],
        deadline=datetime.date(2024, 2, 20),
    )

@pytest.fixture
def scholarship_3():
    return Scholarship(
        title="STEM Scholarship",
        description="Scholarship for STEM students.",
        type="Merit-based",
        country="Canada",
        requirements=["GPA > 3.7", "STEM Major"],
        deadline=datetime.date(2024, 3, 10),
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

def test_filter_by_requirements(scholarship_list):
    """Test filtering scholarships by requirements."""
    gpa_scholarships = Scholarship.filter_by_requirements(scholarship_list, ["GPA > 3.5"])
    assert len(gpa_scholarships) == 2
    assert all("GPA > 3.5" in s.requirements for s in gpa_scholarships)

def test_sort_by_deadline(scholarship_list):
    """Test sorting scholarships by deadline."""
    sorted_scholarships = Scholarship.sort_by_deadline(scholarship_list)
    deadlines = [s.deadline for s in sorted_scholarships]
    assert deadlines == sorted(deadlines)