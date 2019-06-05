from sqlalchemy import Column, Integer, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class Receipt(Base):
    __tablename__ = 'receipt'

    id = Column(Integer, primary_key=True)

    amount = Column(Numeric(7,2))
    date = Column(Date)
    member_id = Column(Integer, ForeignKey('member.id'))

    member = relationship("Member", uselist=False, back_populates='receipts')

    def __repr__(self):
        return "<Receipt(amount='%s', date='%s', member_id='%s')>" % (self.amount, self.date, self.member_id)
