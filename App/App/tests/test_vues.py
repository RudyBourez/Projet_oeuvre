import pytest
from app import app
from app.models import User, Prediction
from flask_login import current_user

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client  
        
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h1> Welcome </h1>' in response.data
    
def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'<h1>Log in</h1>' in response.data
    # Test login with bad identifiers
    response = client.post('/login', data={'email' : "16518", 'password' : "16316"}, follow_redirects=True)
    assert response.request.path == "/login"
    assert not hasattr(current_user, "id")
    # Test login with good identifiers
    response = client.post('/login', data={'email': "admin@example.com", "password": "1234"}, follow_redirects=True)
    assert response.request.path == "/predict"
    assert hasattr(current_user, "id")

def test_logout(client):
    client.post('/login', data={'email': "admin@example.com", "password": "1234"}, follow_redirects=True)
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/"
    assert not hasattr(current_user, "id")
    
def test_predict(client):
    # Connexion to the database
    response = client.post('/login', data={'email': "admin@example.com", "password": "1234"}, follow_redirects=True)
    assert response.request.path == "/predict"
    # Test template
    assert b'<label for="Age_house">' in response.data
    # Test bad post (null values) 
    predictions = Prediction.get_prediction_by_user(current_user.id)
    length_1 = len(predictions)
    response = client.post('/predict', data={'Age_house':None, 'Total Bsmt SF':50, '1st Flr SF':50,
                                             'Gr Liv Area':120,'Garage Area':30, 'Garage Cars':2,
                                             'Overall_Qual':5, 'Bath':2, 'Bsmt Qual':"Good",
                                             'Kitchen Qual': "Excellent", 'Neighborhood': "Crawford"})
    predictions = Prediction.get_prediction_by_user(current_user.id)
    length_2 = len(predictions)
    assert length_2 == length_1
    # Test good post
    response = client.post('/predict', data={'Age_house':10, 'Total Bsmt SF':50, '1st Flr SF':50,
                                             'Gr Liv Area':120,'Garage Area':30, 'Garage Cars':2,
                                             'Overall_Qual':5, 'Bath':2, 'Bsmt Qual':"Good",
                                             'Kitchen Qual': "Excellent", 'Neighborhood': "Crawford"})
    predictions = Prediction.get_prediction_by_user(current_user.id)
    length_3 = len(predictions)
    assert length_3 == length_2 + 1
    # Test value in template
    assert b'La maison vaut: 69880' in response.data
    # Cleaning of the insertion with the test
    Prediction.delete_last_insert_test()
    predictions = Prediction.get_prediction_by_user(current_user.id)
    length_4 = len(predictions)
    assert length_4 == length_2
    
def test_profile(client):
    # Connexion to the database
    client.post('/login', data={'email': "admin@example.com", "password": "1234"})
    response = client.get('/profile')
    # Test template
    assert response.status_code == 200
    assert b'<h1>Profile</h1>' in response.data
    length_predictions = len(Prediction.get_prediction_by_user(current_user.id))
    assert response.data.count(b'<tr>') == length_predictions + 1
    
def test_signup(client):
    response = client.get('/signup')
    # Test Template
    assert response.status_code == 200
    assert b'<h1>Sign Up</h1>' in response.data
    assert b'<form method="POST" action="/signup" class="form">' in response.data
    # Test Post With Email already existing
    length_users_1 = len(User.get_all_user())
    response = client.post('/signup', data={'email': 'admin@example.com','first_name':'test', 'last_name':'test', 'password': '1318641'}, follow_redirects=True)
    length_users_2 = len(User.get_all_user())
    assert length_users_2 == length_users_1
    # Test Post
    response = client.post('/signup', data={'email': 'admin2@example.com','first_name':'test', 'last_name':'test', 'password': '1318641'}, follow_redirects=True)
    length_users_3 = len(User.get_all_user())
    assert length_users_3 == length_users_2 + 1
    assert hasattr(current_user, "id")
    assert response.request.path == '/predict'
    User.drop_user_by_email(email="admin2@example.com")
    length_users_4 = len(User.get_all_user())
    assert length_users_4 == length_users_2