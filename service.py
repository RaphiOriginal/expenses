import cherrypy
import lib.tool.passwordtool
from lib.service.receiptservice import ReceiptService
from lib.service.memberservice import MemberService
from lib.service.householdservice import HouseholdService
from lib.service.accountservice import AccountService

class Service(object):
    @cherrypy.expose
    def index(self):
        return "hi " + str(cherrypy.session['user'])

if __name__ == '__main__':
    from lib.plugin.saplugin import SAEnginePlugin
    SAEnginePlugin(cherrypy.engine, 'sqlite:///database.sqlite').subscribe()

    from lib.plugin.satool import SATool
    cherrypy.tools.db = SATool()

    webapp = Service()
    webapp.account = AccountService()
    webapp.household = HouseholdService()
    webapp.member = MemberService()
    webapp.receipt = ReceiptService()
    cherrypy.quickstart(webapp, '/', 'service.config')
