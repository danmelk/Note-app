from web import create_app
import pytest

from web.models import User

@pytest.fixture(scope = 'module')
def new_user():
    user = User(
        name = 'dan', login = 'danmelk', password = 'qwerty', ip_addr = '129')

    return user

@pytest.fixture(scope = 'module')
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client  

