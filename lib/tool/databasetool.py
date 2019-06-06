import cherrypy
from lib.model.user import User

def db():
    return cherrypy.request.db

def userExists(email):
    return db().query(User).filter_by(email=email).first()
