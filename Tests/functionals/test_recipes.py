
def test_home(test_client):
    response = test_client.get('/home')

    assert response.status_code == 200
    assert response.status_code == 200
    assert b"Welcome to the" in response.data
    assert b"Flask User Management Example!" in response.data
    assert b"Need an account?" in response.data
    assert b"Existing user?" in response.data


def test_home_page_post_with_fixture(test_client):
    response = test_client.post('/')
    
    assert response.status_code == 405
    assert b"Flask User Management Example!" not in response.data