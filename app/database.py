from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://lfl_hoan:lfl_123456@localhost:5432/lfl_db"
 
engine = create_engine(DATABASE_URL, echo=True)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
Base = declarative_base()