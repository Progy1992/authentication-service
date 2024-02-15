from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker


# database connection details
DB_HOSTNAME = "database-2.c5868q8ow48k.us-east-1.rds.amazonaws.com"
DB_USERNAME = "admin"
DB_PASSWORD = "eCKATEPonErcHiPatHLo"
DB_PORT = 3306
DB_NAME = 'books_db'
db_url = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}'

# database connection engine and base for creating ORM objects
Base = declarative_base()
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session_instance = Session()