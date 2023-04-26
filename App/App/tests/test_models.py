from app import *
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import pytest

@pytest.fixture
def my_user1():
    my_user1 = User(first_name="Rudy", last_name='Bourez', email="admin@example.com",
                    password=generate_password_hash('1234', method='sha256'))
    return my_user1

@pytest.fixture
def my_user2():
    my_user2 = User(first_name="User", last_name="User", email="user@example.com",
                    password=generate_password_hash('123456', method='sha256'))
    return my_user2


def test_models(my_user1, my_user2):
    assert my_user1.first_name == "Rudy"
    assert my_user1.last_name == "Bourez"
    assert my_user1.password != '1234'
    assert check_password_hash(my_user1.password, '1234') == True
    assert my_user2.first_name == "User"
    assert my_user2.last_name == "User"
    assert my_user2.password != '123456'
    assert check_password_hash(my_user2.password, '123456') == True