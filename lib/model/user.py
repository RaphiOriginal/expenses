from sqlalchemy import Column, Integer, String, Sequence
from base import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    email = Column(String(255))
    salt = Column(String(255))
    password_hash = Column(String(255))

    def __repr__(self):
        return "<User(email='%s', salt='%s', password_hash='%s')>" % (self.email, self.salt, self.password_hash)
