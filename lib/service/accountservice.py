import cherrypy
from lib.tool.databasetool import userExists, delete, add, findUsersByEmail
from lib.model.user import User
from lib.tool.passwordtool import create_salt, hash_password

@cherrypy.expose
class AccountService(object):
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, email, password):
        exists = userExists(email)
        if exists is None:
            salt = create_salt();
            hashed_password = hash_password(salt, password)
            newUser = User(email=email, salt=salt, password_hash=hashed_password)
            add(newUser)
        else:
            raise cherrypy.HTTPError(409, 'E-Mail already exists')

    @cherrypy.tools.accept(media='text/plain')
    def PUT(self, email, password, new):
        users = findUsersByEmail(email)
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
        users = findUsersByEmail(email)
        if len(users) == 1:
            user = users[0]
            hashed_password = hash_password(user.salt, password)
            if hashed_password == user.password_hash:
                delete(user)
            else:
                raise cherrypy.HTTPError(401, 'Unauthorized')
        else:
            raise cherrypy.HTTPError(500)
