from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ai_onboarding_brain.src.core.config import settings

# Establish SQLAlchemy Engine utilizing connection pooling
engine = create_engine(
    settings.DB_URI,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
