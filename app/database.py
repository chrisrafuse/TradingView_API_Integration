from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (SQLite for local testing)
SQLALCHEMY_DATABASE_URL = "sqlite:///./orders.db"  # SQLite in the current directory

# Create the engine (connects to the database)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # specific to SQLite
)

Base = declarative_base()

# Create a session maker to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
