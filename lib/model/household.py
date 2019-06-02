from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship
from lib.model.member import Member
from lib.model.accessright import AccessRight
from base import Base

class Household(Base):
    __tablename__ = 'household'

    id = Column(Integer, primary_key=True)

    name = Column(String(255))

    members = relationship("Member")
    accessrights = relationship("AccessRight")

    def __repr__(self):
        return "<Household(name='%s')>" % (self.name)
