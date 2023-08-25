from accounts.models import Jwt, User
from django.conf import settings
import secrets, string, jwt, datetime

def get_random(length):
    return "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def get_access_token(payload):
    return jwt.encode(
        {"exp": datetime.datetime.now() + datetime.timedelta(hours=2),"access_token": True, **payload},
        settings.SECRET_KEY,
        algorithm="HS256",
    )

def get_refresh_token():
    return jwt.encode(
       {"exp": datetime.datetime.now() + datetime.timedelta(hours=24),
         "access_token": False,
         },
        settings.SECRET_KEY,
        algorithm="HS256", 
    )

def decodeJWT(bearer):
    if not bearer:
        return None

    token = bearer[7:]

    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None

    if decoded:
        try:
            user = User.objects.get(id=decoded["user_id"])
            jwt_obj = Jwt.objects.filter(user=user)
            if not jwt_obj.exists():
                return None
            return user
        except Exception:
            return None