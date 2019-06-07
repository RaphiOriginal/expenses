import cherrypy
from lib.model.receipt import Receipt
from lib.model.member import Member
from lib.tool.databasetool import add, delete, findReceiptsByHouseholdIds, findReceiptsByHouseholdId, findReceiptById, findMemberById
from lib.tool.authorizationtool import getAuthorizedHouseholdIds

@cherrypy.expose
class ReceiptService(object):
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, amount, r_date, member_id):
        legal_ids = getAuthorizedHouseholdIds()
        member = findMemberById(member_id)
        if member.household.id in legal_ids:
            p_date = datetime.strptime(r_date, '%Y-%m-%d')
            receipt = Receipt(member_id=member_id, date=p_date, amount=amount)
            add(receipt)
        else:
            raise cherrypy.HTTPError(401, 'Unauthorized')

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, receipt_id=None, member_id=None, household_id=None):
        legal_ids = getAuthorizedHouseholdIds()
        if receipt_id is None and member_id is None and household_id is None:
            receipts = findReceiptsByHouseholdIds(legal_ids)
            return str(receipts)
        elif household_id is not None and int(household_id) in legal_ids:
            receipts = findReceiptsByHouseholdId(household_id)
            return str(receipts)
        elif member_id is not None:
            member = findMemberById(member_id)
            if member.household_id in legal_ids:
                return str(member.receipts)
            else:
                raise cherrypy.HTTPException(401, 'Unauthorized')
        else:
            receipt = findReceiptById(receipt_id)
            if receipt.member.household_id in legal_ids:
                return str(receipt)
            else:
                raise cherrypy.HTTPException(401, 'Unauthorized')

    @cherrypy.tools.accept(media='text/plain')
    def PUT(self, id, date, amount):
        legal_ids = getAuthorizedHouseholdIds()
        receipt = findReceiptById(id)
        if receipt.member.household_id in legal_ids:
            p_date = datetime.strptime(date, '%Y-%m-%d')
            receipt.date = p_date
            receipt.amount = amount
        else:
            raise cherrypy.HTTPError(401, 'Unauthorized')

    cherrypy.tools.accept(media='text/plain')
    def DELETE(self, id):
        legal_ids = getAuthorizedHouseholdIds()
        receipt = findReceiptById(id)
        if receipt.member.household_id in legal_ids:
            delete(receipt)
        else:
            raise cherrypy.HTTPError(401, 'Unauthorized')
