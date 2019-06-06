import cherrypy
import hashlib, uuid
from datetime import datetime
from cherrypy.lib import auth_basic
from lib.model.user import User

def create_salt():
    return uuid.uuid4().hex

def hash_password(salt, password):
    return hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

def is_valid_password(user, password):
    salt = user.salt
    to_check = hash_password(salt, password)
    return to_check == user.password_hash

def checkpassword(realm, email, password):
    cherrypy.tools.db.bind_session()
    db = cherrypy.request.db
    user = db.query(User).filter_by(email=email).one()
    if is_valid_password(user, password):
        cherrypy.session['user'] = user
        return True
    else:
        return False
