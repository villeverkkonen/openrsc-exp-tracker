from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

LOCAL_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432"
engine = create_engine(os.environ.get("DATABASE_URL", LOCAL_DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
