import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    def __init__(self, DATABASE_URL):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(
            autoflush=False, autocommit=False, bind=self.engine
        )

    def get_db(self):
        """Dependency Injection: Yields a new session and ensures proper closure."""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def connect(self):
        """Creates database tables if they don't exist and handles connection."""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database connected")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")

    def disconnect(self):
        """Properly disposes of the engine to release resources."""
        try:
            self.engine.dispose()
            logger.info("Database disconnected")
        except Exception as e:
            logger.error(f"Database disconnection failed: {e}")


# Initialize database instance
DB_URL = os.getenv("DATABASE_URL")
DB = Database(DB_URL)
