import cherrypy
from lib.service.receiptservice import ReceiptService
from lib.service.memberservice import MemberService
from lib.service.householdservice import HouseholdService
from lib.service.accountservice import AccountService
import hashlib, uuid
from datetime import datetime
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
    if is_valid_password(user, password):
        cherrypy.session['user'] = user
        return True
    else:
        return False

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
