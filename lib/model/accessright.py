from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class AccessRight(Base):
    __tablename__ = 'accessright'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    household_id = Column(Integer, ForeignKey('household.id'))

    user = relationship("User", uselist=False, back_populates='accessright')
    household = relationship("Household", uselist=False, back_populates='accessright')

    def __repr__(self):
        return "<AccessRight(user_id='%s', household_id='%s')" % (self.user_id, self.household_id)
