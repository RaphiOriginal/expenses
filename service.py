import cherrypy

@cherrypy.expose
class ExpensesService(object):
    
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return 'Hello World'

if __name__ == '__main__':
    conf = {
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/plain')],
                }
            }
    cherrypy.quickstart(ExpensesService(), '/', conf)
