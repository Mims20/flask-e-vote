import pytest
from app import create_app, db
from app.config import settings
from app.models import User, Candidate


@pytest.fixture(scope="session")
def app():
    app = create_app()

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{settings.database_username}:{settings.database_password}" \
                                            f"@{settings.database_hostname}:{settings.database_port}/" \
                                            f"{settings.database_name}_test"
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF protection for testing

    with app.app_context():
        # Set up any necessary database or other resources
        db.drop_all()
        db.create_all()

        yield app

        # Teardown and clean up resources
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def dummy_user(client, app):
    data = {"email": "test@test.com", "password": "password123"}

    client.post("/register", data=data)

    yield data

    # Rollback changes made within the current session
    db.session.rollback()

    # Execute database-specific commands or scripts to reset the auto-incremented counter
    # Example command for PostgreSQL:
    db.session.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1;")
    db.session.commit()


@pytest.fixture(scope="function")
def login_dummy_user(client, dummy_user):
    client.post("/login", data={"email": dummy_user["email"], "password": dummy_user["password"]})

    yield

    client.get("/logout")


@pytest.fixture()
def add_candidate1(client, login_dummy_user):
    # Define test data
    candidate_data = {
        "first_name": "John",
        "last_name": "Doe",
        "position": "President",
        "image": "JkldMniewlsXZq"
    }

    new_candidate = Candidate(**candidate_data)
    db.session.add(new_candidate)
    db.session.commit()


@pytest.fixture()
def add_candidate2(client, login_dummy_user):
    # Define test data
    candidate_data = {
        "first_name": "Mike",
        "last_name": "Peters",
        "position": "Secretary",
        "image": "JklGkLwnalsXZq"
    }

    new_candidate = Candidate(**candidate_data)
    db.session.add(new_candidate)
    db.session.commit()
