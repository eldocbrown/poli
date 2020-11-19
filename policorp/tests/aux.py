from policorp.models import User

def createUser(username, email, password):
    u = User()
    u.username = username
    u.email = email
    u.set_password(password)
    u.save()
    return u
