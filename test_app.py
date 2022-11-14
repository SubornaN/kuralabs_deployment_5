from application import app, greet

def test_home_page():
    response = app.test_client().get('/')
    assert response.status_code == 200
    
def test_invalid_url():
    response = app.test_client().get('youtube.com')
    assert response.status_code == 404
    
def test_saved_url():
    response = app.test_client().get('/house')
    assert response.status_code == 302