import json
import datetime
from json import JSONEncoder
from policorp.models import User

def createUser(username, email, password):
    u = User()
    u.username = username
    u.email = email
    u.set_password(password)
    u.save()
    return u

# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
