from sqlalchemy import Column, Integer, String, ForeignKey
from base import Base

class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    household_id = Column(Integer, ForeignKey('household.id'))

    def __repr__(self):
        return "<Member(name='%s')>" % self.name
