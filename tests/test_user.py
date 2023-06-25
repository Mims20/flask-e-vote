from flask_login import current_user

from app.forms.forms import RegisterForm, LoginForm
from app.models import User


def test_user_creation(client, app):
    with app.app_context():
        form = RegisterForm()

        form.email.data = "test@example.com"
        form.password.data = "password123"
        form.confirm_password.data = "password123"

        response = client.post('/register', json=form.data, follow_redirects=True)
        assert response.status_code == 200
        # assert b"Registration Successful. Please Login." in response.data

        with app.app_context():
            assert User.query.count() == 1
            user = User.query.filter_by(email=form.email.data).first()
            # assert user is not None
            assert user.email == form.email.data


def test_login_dummy_user(client, dummy_user):
    form = LoginForm()
    form.email.data = "test@test.com"
    form.password.data = "password123"

    response = client.post("/login", data=form.data)
    assert response.status_code == 302
    assert current_user.is_authenticated
    assert current_user.id == 1


def test_logout_dummy_user(client, dummy_user, login_dummy_user):
    response = client.get("/logout")
    assert response.status_code == 302
    assert current_user.is_authenticated == False
