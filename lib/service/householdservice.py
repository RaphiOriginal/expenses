import cherrypy
from lib.model.household import Household
from lib.model.accessright import AccessRight

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
