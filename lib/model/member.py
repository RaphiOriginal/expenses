from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    household_id = Column(Integer, ForeignKey('household.id'))

    household = relationship("Household", back_populates="member")

    def __repr__(self):
        return "<Member(name='%s')>" % self.name
