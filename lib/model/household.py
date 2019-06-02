from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from lib.model.member import Member

Base = declarative_base()

class Household(Base):
    __tablename__ = 'household'

    id = Column(Integer, primary_key=True)

    name = Column(String(255))

    members = relationship("Member", order_by=Member.id, back_populates="household")

    def __repr__(self):
        return "<Household(name='%s')>" % (self.name)
