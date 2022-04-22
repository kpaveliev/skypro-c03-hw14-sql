import pytest
from dao import NetflixDAO
from config import DB_NETFLIX

@pytest.fixture()
def netflix_db():
    return NetflixDAO(DB_NETFLIX)

@pytest.fixture()
def correct_keys():
    return {'title', 'country', 'release_year', 'genre', 'description'}