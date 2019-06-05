import cherrypy
from lib.model.user import User
from lib.model.household import Household
from lib.model.member import Member
from lib.model.accessright import AccessRight
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
    if is_valid_password(user, password):
        cherrypy.session['user'] = user
        return True
    else:
        return False

class Service(object):
    @cherrypy.expose
    def index(self):
        return "hi " + str(cherrypy.session['user'])

@cherrypy.expose
class AccountService(object):
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

    @cherrypy.tools.accept(media='text/plain')
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

    @cherrypy.tools.accept(media='text/plain')
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

@cherrypy.expose
class HouseholdService(object):
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, name):
        db = cherrypy.request.db
        user = cherrypy.session['user']
        if user is None:
            raise cherrypy.HTTPError(401, 'Unauthorized')
        household = Household(name = name)
        db.add(household)
        db.commit()
        access_right = AccessRight(user_id=user.id, household_id=household.id)
        db.add(access_right)
        return str(household)

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, id=None):
        db = cherrypy.request.db
        user = cherrypy.session['user']
        if user is None:
            raise cherrypy.HTTPError(401, 'Unauthorized')
        accessrights = user.accessrights
        print("DEBUG: Accessrights to" + str(accessrights))
        if accessrights is None or len(accessrights) == 0:
            raise cherrypy.HTTPError(401, 'Unauthorized')
        if id is None:
            households = []
            print("DEBUG: " + str(accessrights))
            for accessright in accessrights:
                h = db.query(Household).filter(Household.id == accessright.household_id).one()
                households.append(h)
            return str(households)
        else:
            access_ids = list(map(lambda x: int(x.household_id), accessrights))
            if int(id) in access_ids:
                household = db.query(Household).filter_by(id=id).one()
                return str(household)
            else:
                raise cherrypy.HTTPError(401, 'Unauthorized')

    @cherrypy.tools.accept(media='text/plain')
    def PUT(self, id, name):
        db = cherrypy.request.db
        user = cherrypy.session['user']
        if user is None:
            raise cherrypy.HTTPError(401, 'Unauthorized')
        legal_ids = list(map(lambda x: int(x.household_id), user.accessrights))
        print("DEBUG: " + str(legal_ids))
        if int(id) in legal_ids:
            household = db.query(Household).filter(Household.id == id).one()
            household.name = name
        else:
            raise cherrypy.HTTPError(401,  'Unaouthorized')

    @cherrypy.tools.accept(media='text/plain')
    def DELETE(self, id):
        db = cherrypy.request.db
        user = cherrypy.session['user']
        if user is None:
            raise cherrypy.HTTPError(401, 'Unauthorized')
        legal_ids = list(map(lambda x: int(x.household_id), user.accessrights))
        if int(id) in legal_ids:
            household = db.query(Household).filter(Household.id == id).one()
            db.delete(household)

@cherrypy.expose
class MemberService(object):

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, name, household_id):
        db = cherrypy.request.db
        user = cherrypy.session['user']
        if user is None:
            raise cherrypy.HTTPError(401, 'Unauthorized')
        legal_ids = list(map(lambda x: int(x.household_id), user.accessrights))
        if int(household_id) in legal_ids:
            member = Member(name = name, household_id = int(household_id))
            db.add(member)
        else:
            raise cherrypy.HTTPError(401, 'Unauthorized')

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, id=None, household_id=None):
        db = cherrypy.request.db
        user = cherrypy.session['user']
        if user is None:
            raise cherrypy.HTTPError(401, 'Unauthorized')
        legal_ids = list(map(lambda x: int(x.household_id), user.accessrights))
        if id is None and household_id is None:
            members = db.query(Member).filter(Member.household_id.in_(legal_ids)).all()
            return str(members)
        elif id is None and int(household_id) in legal_ids:
            members = db.query(Member).filter(Member.household_id == household_id).all()
            return str(members)
        else:
            member = db.query(Member).filter(Member.id == id).one()
            h_id = member.household.id
            if h_id in legal_ids:
                return str(member)
            else:
                raise cherrypy.HTTPError(401, 'Unauthorized')

    @cherrypy.tools.accept(media='text/plain')
    def PUT(self, id, name):
        db = cherrypy.request.db
        user = cherrypy.session['user']
        if user is None:
            raise cherrypy.HTTPError(401, 'Unauthorized')
        legal_ids = list(map(lambda x: int(x.household_id), user.accessrights))
        member = db.query(Member).filter(Member.id == id).one()
        h_id = member.household.id
        if h_id in legal_ids:
            member.name = name
        else:
            raise cherrypy.HTTPError(401, 'Unauthorized')

    @cherrypy.tools.accept(media='text/plain')
    def DELETE(self, id):
        db = cherrypy.request.db
        user = cherrypy.session['user']
        if user is None:
            raise cherrypy.HTTPError(401, 'Unauthorized')
        legal_ids = list(map(lambda x: int(x.household_id), user.accessrights))
        member = db.query(Member).filter(Member.id == id).one()
        h_id = member.household_id
        if h_id in legal_ids:
            db.delete(member)
        else:
            raise cherrypy.HTTPError(401, 'Unauthorized')

@cherrypy.expose
class ReceiptService(object):
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, amount, date, member_id):
        db = cherrypy.request.db
        user = cherrypy.session['user']
        if user is None:
            raise cherrypy.HTTPError(401, 'Unautorized')
        legal_ids = list(map(lambda x: int(x.household_id), user.accessrights))
        member = db.query(Member).filter(Member.id == member_id).one()
        if member.household.id in legal_ids:
            receipt = Receipt(member_id=member_id, date=date, amount=amount)
            db.add(receipt)
        else:
            raise cherrypy.HTTPError(401, 'Unauthorized')

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
