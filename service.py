import cherrypy
from lib.model.user import User
from lib.model.household import Household
from lib.model.member import Member
import hashlib, uuid
from cherrypy.lib import auth_basic

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
    return is_valid_password(user, password)

class Service(object):
    @cherrypy.expose
    def index(self):
        return "hi"

@cherrypy.expose
class Account(object):
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, email, password):
        db = cherrypy.request.db
        exists = db.query(User).filter_by(email=email).first()
        if exists is None:
            salt = create_salt();
            hashed_password = hash_password(salt, password)
            newUser = User(email=email, salt=salt, password_hash=hashed_password)
            db.add(newUser)
        else:
            raise cherrypy.HTTPError(409, 'E-Mail already exists')

    def PUT(self, email, password, new):
        db = cherrypy.request.db
        users = db.query(User).filter_by(email=email).all()
        if len(users) == 1:
            user = users[0]
            hashed_password = hash_password(user.salt, password)
            if hashed_password == user.password_hash:
                salt = create_salt()
                new_hash = hash_password(salt, new)
                user.salt = salt
                user.password_hash = new_hash
            else:
                raise cherrypy.HTTPError(401, 'Unauthorized')
        else:
            raise cherrypy.HTTPError(500)

        def DELETE(self, email, password):
            db = cherrypy.request.db
            users = db.query(User).filter_by(email=email).all()
            if len(users) == 1:
                user = users[0]
                hashed_password = hash_password(user.salt, password)
                if hashed_password == user.password_hash:
                    db.delete(user)
                else:
                    raise cherrypy.HTTPError(401, 'Unauthorized')
            else:
                raise cherrypy.HTTPError(500)

if __name__ == '__main__':
    from lib.plugin.saplugin import SAEnginePlugin
    SAEnginePlugin(cherrypy.engine, 'sqlite:///database.sqlite').subscribe()

    from lib.plugin.satool import SATool
    cherrypy.tools.db = SATool()

    conf = {
            '/': {
                'tools.sessions.on': True,
                'tools.auth_basic.on': True,
                'tools.auth_basic.realm': 'Expenses',
                'tools.auth_basic.checkpassword': checkpassword,
                },
            '/account': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/plain')],
                'tools.db.on': True,
                }
            }

    webapp = Service()
    webapp.account = Account()
    cherrypy.quickstart(webapp, '/', conf)
