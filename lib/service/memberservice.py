import cherrypy
from lib.model.member import Member
from lib.tool.databasetool import add, delete, findMembersByHouseholdIds, findMembersByHouseholdId, findMemberById

@cherrypy.expose
class MemberService(object):

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, name, household_id):
        user = cherrypy.session['user']
        if user is None:
            raise cherrypy.HTTPError(401, 'Unauthorized')
        legal_ids = list(map(lambda x: int(x.household_id), user.accessrights))
        if int(household_id) in legal_ids:
            member = Member(name = name, household_id = int(household_id))
            add(member)
        else:
            raise cherrypy.HTTPError(401, 'Unauthorized')

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, id=None, household_id=None):
        user = cherrypy.session['user']
        if user is None:
            raise cherrypy.HTTPError(401, 'Unauthorized')
        legal_ids = list(map(lambda x: int(x.household_id), user.accessrights))
        if id is None and household_id is None:
            members = findMembersByHouseholdIds(legal_ids)
            return str(members)
        elif id is None and int(household_id) in legal_ids:
            members = findMembersByHouseholdId(household_id)
            return str(members)
        else:
            member = findMemberById(id)
            h_id = member.household.id
            if h_id in legal_ids:
                return str(member)
            else:
                raise cherrypy.HTTPError(401, 'Unauthorized')

    @cherrypy.tools.accept(media='text/plain')
    def PUT(self, id, name):
        user = cherrypy.session['user']
        if user is None:
            raise cherrypy.HTTPError(401, 'Unauthorized')
        legal_ids = list(map(lambda x: int(x.household_id), user.accessrights))
        member = findMemberById(id)
        h_id = member.household.id
        if h_id in legal_ids:
            member.name = name
        else:
            raise cherrypy.HTTPError(401, 'Unauthorized')

    @cherrypy.tools.accept(media='text/plain')
    def DELETE(self, id):
        user = cherrypy.session['user']
        if user is None:
            raise cherrypy.HTTPError(401, 'Unauthorized')
        legal_ids = list(map(lambda x: int(x.household_id), user.accessrights))
        member = findMemberById(id)
        h_id = member.household_id
        if h_id in legal_ids:
            delete(member)
        else:
            raise cherrypy.HTTPError(401, 'Unauthorized')
