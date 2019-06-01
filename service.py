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

@cherrypy.expose
class ExpensesService(object):
    
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, email, password):
        db = cherrypy.request.db
        salt = create_salt();
        hashed_password = hash_password(salt, password)
        newUser = User(email=email, salt=salt, password_hash=hashed_password)
        db.add(newUser)
        return str(db.query(User).filter_by(email=email).first())

    @cherrypy.tools.authenticate()
    def GET(self, email, password):
        db = cherrypy.request.db
        user = db.query(User).filter_by(email=email).first()
        hashed_password = hash_password(user.salt, password)
        if hashed_password == user.password_hash:
            return "Authentificated"
        else:
            return "Wroooong!"

if __name__ == '__main__':
    from lib.plugin.saplugin import SAEnginePlugin
    SAEnginePlugin(cherrypy.engine, 'sqlite:///database.sqlite').subscribe()

    from lib.plugin.satool import SATool
    cherrypy.tools.db = SATool()

    conf = {
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/plain')],
                'tools.db.on': True,
                }
            }
    cherrypy.quickstart(ExpensesService(), '/', conf)
