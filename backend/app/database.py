import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./realityverse.db")

# sqlite-specific configuration to allow multi-threaded access in FastAPI
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def init_db():
    """Create all tables defined in SQLModel metadata."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency generator for database sessions in FastAPI."""
    with Session(engine) as session:
        yield session
