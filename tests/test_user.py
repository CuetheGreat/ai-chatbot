import pytest # type: ignore
from app.database import Database, Base
from app.models import User
import os
from dotenv import load_dotenv  # type: ignore
from sqlalchemy.orm import sessionmaker


from app.models.user import User


load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
DB = Database(DB_URL)

@pytest.fixture(scope="module")
def db():
    """ Database fixture that sets up and tears down the database for testing. """
    DB.connect()
    Base.metadata.drop_all(bind=DB.engine)
    Base.metadata.create_all(bind=DB.engine)
    yield DB
    Base.metadata.drop_all(bind=DB.engine)
    DB.disconnect()

@pytest.fixture(scope="function")
def session(db):
    """ Creates a new database session for each test and rolls back after execution. """
    SessionLocal = sessionmaker(bind=db.engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(scope="module")
def new_user():
    """Fixture to create a new user instance without persisting it to the database."""
    return User(username="testuser", email="test@example.com", password="password")

def test_user_creation(new_user):
    """Test that a new user object is created correctly"""
    assert new_user.username == "testuser"
    assert new_user.email == "test@example.com"
    assert new_user.password == "password"  # Consider hashing passwords in actual tests
    assert new_user.id is None  # User ID should be None before committing to the DB

def test_create_user(session):
    """ Test creating a user """
    new_user = User(username="testuser", email="testuser@example.com", password="password")
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    assert new_user.id is not None


def test_read_user(session):
    """ Test reading a user """
    user = session.query(User).filter_by(username="testuser").first()

    assert user is not None
    assert user.username == "testuser"


def test_update_user(session):
    """ Test updating a user """
    user = session.query(User).filter_by(username="testuser").first()
    assert user is not None

    user.email = "newemail@example.com"
    session.commit()

    updated_user = session.query(User).filter_by(username="testuser").first()
    assert updated_user.email == "newemail@example.com"


def test_delete_user(session):
    """ Test deleting a user """
    user = session.query(User).filter_by(username="testuser").first()
    assert user is not None

    session.delete(user)
    session.commit()

    deleted_user = session.query(User).filter_by(username="testuser").first()
    assert deleted_user is None
