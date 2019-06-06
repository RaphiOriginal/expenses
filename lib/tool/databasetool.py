import cherrypy
from lib.model.user import User
from lib.model.member import Member
from lib.model.household import Household

def db():
    return cherrypy.request.db

def userExists(email):
    return db().query(User).filter_by(email=email).first()

def delete(object):
    db().delete(object)

def add(object):
    db().add(object)

def commit():
    db().commit()

def findUsersByEmail(email):
    return db().query(User).filter_by(email=email).all()

def findHouseholdById(id):
    return db().query(Household).filter(Household.id == id).one()

def findMembersByHouseholdIds(ids):
    return db().query(Member).filter(Member.household_id.in_(ids)).all()

def findMemberById(id):
    return db().query(Member).filter(Member.id == id).one()

def findMembersByHouseholdId(id):
    return db().query(Member).filter(Member.household_id == id).all()
