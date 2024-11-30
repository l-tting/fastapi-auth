from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./auth.db'

# echo - logs every query -for debugging
engine = create_engine(SQLALCHEMY_DATABASE_URL,echo=True)
# session is an env to interact with db
# after creating a session it will automatically use the engine to executte queries on connected db
session_local = sessionmaker(bind=engine)

Base = declarative_base()

''' 
dependency injection for handling db sessions
creates new session for each request and ensures its closed after request is processed
'''
def get_db():
    # creates new database session
    db = session_local()
    try:
        # yields /gives session to route handler and lets it execute db operations in route
        yield db
    finally:
        # ensures session is closed after execution
        db.close()