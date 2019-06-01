import cherrypy
from lib.model.user import User

@cherrypy.expose
class ExpensesService(object):
    
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        db = cherrypy.request.db
        test = User(email='bla', salt='1', password_hash='1234')
        db.add(test)
        return str(db.query(User).first())

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
