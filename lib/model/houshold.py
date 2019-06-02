from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Household(Base):
    __tablename__ = 'household'

    id = Column(Integer, primary_key=True)

    name = Column(String(255))

    def __repr__(self):
        return "<Household(name='%s')>" % (self.name)
