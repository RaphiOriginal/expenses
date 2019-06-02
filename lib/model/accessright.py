from sqlalchemy import Column, Integer, ForeignKey
from base import Base

class AccessRight(Base):
    __tablename__ = 'accessright'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    household_id = Column(Integer, ForeignKey('houesehold.id'))

    def __repr__(self):
        return "<AccessRight(user_id='%s', household_id='%s')" % (self.user_id, self.household_id)
