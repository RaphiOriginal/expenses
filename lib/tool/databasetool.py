import cherrypy
from lib.model.user import User

def db():
    return cherrypy.request.db

def userExists(email):
    return db().query(User).filter_by(email=email).first()

def delete(object):
    db().delete(object)

def add(object):
    db().add(object)

def findUsersByEmail(email):
    return db().query(User).filter_by(email=email).all()
