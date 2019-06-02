from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)

    name = Column(varchar(255))
    household_id = Column(Integer, ForeignKey('household.id'))

    household = relationship("Household", back_populates="member")

    def __repr__(self):
        return "<Member(name='%s')>" % self.name
