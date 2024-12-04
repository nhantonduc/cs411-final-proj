import pytest

# from scholarship_finder.models.scholarships_model import Scholarship
# from scholarship_finder.models.favorites_model import FavoritesModel

@pytest.fixture()
def favorites_model():
    """Fixture to provide a new empty instance of FavoritesModel for each test."""
    return FavoritesModel(1, [])

"""Fixtures providing sample favorites lists for the tests."""
@pytest.fixture
def sample_id1():
    return 1111

@pytest.fixture
def sample_id2():
    return 2222

# Testing add_to_favorites
def test_add_to_favorites(favorites_model, sample_id1, sample_id2):
    """Test adding scholarships from favorites list"""
    assert len(favorites_model.favorites) == 0
    favorites_model.add_to_favorites(sample_id1)
    assert len(favorites_model.favorites) == 1
    assert favorites_model.favorites[0] == sample_id1
    favorites_model.add_to_favorites(sample_id2)
    assert len(favorites_model.favorites) == 2
    assert favorites_model.favorites[1] == sample_id2

# Testing remove_from_favorites
def test_remove_from_favorites(favorites_model, sample_id1, sample_id2):
    """Test removing scholarships from favorites list"""
    favorites_model.favorites.append(sample_id1)
    favorites_model.favorites.append(sample_id2)
    assert len(favorites_model.favorites) == 2
    favorites_model.remove_from_favorites(sample_id1)
    assert len(favorites_model.favorites) == 1
    favorites_model.remove_from_favorites(sample_id2)
    assert len(favorites_model.favorites) == 0

# Testing get_favorites
def test_get_favorites(favorites_model, sample_id1, sample_id2):
    """Test retrieving favorites lists with scholarships in it"""
    favorites_model.favorites.append(sample_id1)
    favorites_model.favorites.append(sample_id2)
    retrieved_favorites = favorites_model.get_favorites()
    assert len(retrieved_favorites) == 2
    assert retrieved_favorites[0] == sample_id1
    assert retrieved_favorites[1] == sample_id2

# Testing clear_favorites
def test_clear_favorites(favorites_model, sample_id1, sample_id2):
    """Test clearing favorites lists with scholarships in it"""
    assert len(favorites_model.favorites) == 0 # should be empty
    favorites_model.favorites.append(sample_id1)
    favorites_model.favorites.append(sample_id2)
    assert len(favorites_model.favorites) == 2 # should have two ids
