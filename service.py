import cherrypy

@cherrypy.expose
class ExpensesService(object):
    
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        db = cherrypy.request.db
        return 'Hello World'

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
                }
            }
    cherrypy.quickstart(ExpensesService(), '/', conf)
