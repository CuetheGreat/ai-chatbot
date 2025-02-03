import pytest # type: ignore
from app.database import Database, Base
from app.models import User
import os
from dotenv import load_dotenv  # type: ignore
from sqlalchemy.orm import sessionmaker

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


def test_connect(db):
    """ Test if the database is connected """
    assert db.engine is not None

def test_disconnect(db):
    """Test if the database is properly disconnected"""
    db.disconnect()

    try:
        # Attempting to use the engine should fail after disconnecting
        connection = db.engine.connect()
    except Exception as e:
        disconnected = True
    else:
        disconnected = False
        connection.close()

    assert disconnected, "Database engine should not allow new connections after disconnecting."
