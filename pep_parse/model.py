from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Pep(Base):
    __tablename__ = "pep"

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    name = Column(String(250))
    status = Column(String(50))
