import cherrypy
from lib.model.member import Member

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
