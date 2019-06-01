import cherrypy
from lib.model.user import User
import hashlib, uuid

def create_salt():
    return uuid.uuid4().hex

def hash_password(salt, password):
    return hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

@cherrypy.tools.register('on_start_resource')
def authenticate():
    print("I'm called now")

class Service(object):
    @cherrypy.expose
    def index(self):
        return "hi"

@cherrypy.expose
class Account(object):
    @cherrypy.tools.accept(media='text/plain')
    def PUT(self, email, password):
        db = cherrypy.request.db
        exists = db.query(User).filter_by(email=email).first()
        if exists is None:
            salt = create_salt();
            hashed_password = hash_password(salt, password)
            newUser = User(email=email, salt=salt, password_hash=hashed_password)
            db.add(newUser)
        else:
            raise cherrypy.HTTPError(409, 'E-Mail already exists')

    @cherrypy.tools.authenticate()
    def GET(self, email, password):
        db = cherrypy.request.db
        user = db.query(User).filter_by(email=email).first()
        hashed_password = hash_password(user.salt, password)
        if hashed_password == user.password_hash:
            return "Authenticated"
        else:
            return "Wroooong!"

if __name__ == '__main__':
    from lib.plugin.saplugin import SAEnginePlugin
    SAEnginePlugin(cherrypy.engine, 'sqlite:///database.sqlite').subscribe()

    from lib.plugin.satool import SATool
    cherrypy.tools.db = SATool()

    conf = {
            '/': {
                'tools.sessions.on': True,
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
