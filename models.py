from sqlalchemy import Column,Integer,String
from database import Base,engine


class User(Base):
    __tablename__='users'
    user_id = Column(Integer,primary_key=True)
    full_name = Column(String,nullable=False)
    username = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)



