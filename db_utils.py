from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Application

# Create SQLite database
DATABASE_URL = "sqlite:///applications.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create all tables
Base.metadata.create_all(engine)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_application(job_title, company_name, status, notes):
    """Add a new job application to the database."""
    session = SessionLocal()
    try:
        new_app = Application(
            job_title=job_title,
            company_name=company_name,
            status=status,
            notes=notes
        )
        session.add(new_app)
        session.commit()
    finally:
        session.close()

def list_applications():
    """Return all job applications."""
    session = SessionLocal()
    try:
        return session.query(Application).all()
    finally:
        session.close()
