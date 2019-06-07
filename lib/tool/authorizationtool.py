import cherrypy

def authorize():
    user = cherrypy.session['user']
    if user is None:
        raise cherrypy.HTTPError(401, 'Unauthorized')
    return user

def getAuthorizedHouseholdIds():
    user = authorize()
    return list(map(lambda x: int(x.household_id), user.accessrights))
