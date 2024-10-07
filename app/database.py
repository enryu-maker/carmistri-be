from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQL_DATABASE_URL = "postgresql://postgres:admin@localhost/carmistridb"
engine = create_engine(SQL_DATABASE_URL)

SessionLocale = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
