"""
FinTrack Pro - Database setup and session management
SQLite + SQLAlchemy
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, Category

# Database file in project root
DB_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(DB_DIR, 'fintrack.db')}"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    """Return a new database session."""
    return SessionLocal()


def init_db():
    """Create all tables and seed default categories if empty."""
    Base.metadata.create_all(bind=engine)
    session = get_session()
    try:
        if session.query(Category).count() == 0:
            default_categories = [
                Category(name="Food"),
                Category(name="Transport"),
                Category(name="Utilities"),
                Category(name="Entertainment"),
                Category(name="Shopping"),
                Category(name="Health"),
                Category(name="Other"),
            ]
            session.add_all(default_categories)
            session.commit()
    finally:
        session.close()
