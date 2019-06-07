import cherrypy
from lib.model.household import Household
from lib.model.accessright import AccessRight
from lib.tool.databasetool import add, commit, delete, findHouseholdById
from lib.tool.authorizationtool import getAuthorizedHouseholdIds, authorize

@cherrypy.expose
class HouseholdService(object):
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, name):
        user = authorize()
        household = Household(name = name)
        add(household)
        commit()
        access_right = AccessRight(user_id=user.id, household_id=household.id)
        add(access_right)
        return str(household)

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, id=None):
        user = authorize()
        accessrights = user.accessrights
        print("DEBUG: Accessrights to" + str(accessrights))
        if accessrights is None or len(accessrights) == 0:
            raise cherrypy.HTTPError(401, 'Unauthorized')
        if id is None:
            households = []
            print("DEBUG: " + str(accessrights))
            for accessright in accessrights:
                h = findHouseholdById(accessright.household_id)
                households.append(h)
            return str(households)
        else:
            access_ids = list(map(lambda x: int(x.household_id), accessrights))
            if int(id) in access_ids:
                household = findHouseholdById(id)
                return str(household)
            else:
                raise cherrypy.HTTPError(401, 'Unauthorized')

    @cherrypy.tools.accept(media='text/plain')
    def PUT(self, id, name):
        user = authorize()
        legal_ids = getAuthorizedHouseholdIds()
        print("DEBUG: " + str(legal_ids))
        if int(id) in legal_ids:
            household = findHouseholdById(id)
            household.name = name
        else:
            raise cherrypy.HTTPError(401,  'Unaouthorized')

    @cherrypy.tools.accept(media='text/plain')
    def DELETE(self, id):
        user = authorize()
        legal_ids = getAuthorizedHouseholdIds()
        if int(id) in legal_ids:
            household = findHouseholdById(id)
            delete(household)
