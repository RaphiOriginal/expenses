from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    household_id = Column(Integer, ForeignKey('household.id'))

    household = relationship("Household", uselist=False, back_populates='members')

    def __repr__(self):
        return "<Member(name='%s')>" % self.name
