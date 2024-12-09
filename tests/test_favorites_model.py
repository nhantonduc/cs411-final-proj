import pytest

from scholarship_finder.models.scholarship_model import Scholarship
from scholarship_finder.models.favorites_model import FavoritesModel

@pytest.fixture()
def favorites_model():
    """Fixture to provide a new empty instance of FavoritesModel for each test."""
    return FavoritesModel(1, [])

@pytest.fixture
def sample_scholarship1():
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
def sample_scholarship2():
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

def test_add_to_favorites(favorites_model, sample_scholarship1, sample_scholarship2):
    """Test adding scholarships to favorites list"""
    assert len(favorites_model.favorites) == 0
    favorites_model.add_to_favorites(sample_scholarship1)
    assert len(favorites_model.favorites) == 1
    assert favorites_model.favorites[0].scholarship_name == "Merit Scholarship"
    favorites_model.add_to_favorites(sample_scholarship2)
    assert len(favorites_model.favorites) == 2
    assert favorites_model.favorites[1].scholarship_name == "Need Scholarship"

def test_remove_from_favorites(favorites_model, sample_scholarship1, sample_scholarship2):
    """Test removing scholarships from favorites list"""
    favorites_model.add_to_favorites(sample_scholarship1)
    favorites_model.add_to_favorites(sample_scholarship2)
    assert len(favorites_model.favorites) == 2
    favorites_model.remove_from_favorites(sample_scholarship1)
    assert len(favorites_model.favorites) == 1
    assert favorites_model.favorites[0].scholarship_name == "Need Scholarship"
    favorites_model.remove_from_favorites(sample_scholarship2)
    assert len(favorites_model.favorites) == 0

def test_get_favorites(favorites_model, sample_scholarship1, sample_scholarship2):
    """Test retrieving favorites list with scholarships in it"""
    favorites_model.add_to_favorites(sample_scholarship1)
    favorites_model.add_to_favorites(sample_scholarship2)
    retrieved_favorites = favorites_model.get_favorites()
    assert len(retrieved_favorites) == 2
    assert retrieved_favorites[0].scholarship_name == "Merit Scholarship"
    assert retrieved_favorites[1].scholarship_name == "Need Scholarship"

def test_clear_favorites(favorites_model, sample_scholarship1, sample_scholarship2):
    """Test clearing favorites list with scholarships in it"""
    assert len(favorites_model.favorites) == 0  # should be empty
    favorites_model.add_to_favorites(sample_scholarship1)
    favorites_model.add_to_favorites(sample_scholarship2)
    assert len(favorites_model.favorites) == 2  # should have two scholarships
    favorites_model.clear_favorites()
    assert len(favorites_model.favorites) == 0  # should be empty again
