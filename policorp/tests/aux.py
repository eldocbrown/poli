import json
import datetime
from json import JSONEncoder
from policorp.models import User

def createUser(username, email, password, first_name=None, last_name=None):
    u = User()
    u.username = username
    u.email = email
    if first_name != None:
        u.first_name = first_name
    if last_name != None:
        u.last_name = last_name
    u.set_password(password)
    u.save()
    return u

# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
