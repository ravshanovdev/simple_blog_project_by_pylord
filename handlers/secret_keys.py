import jwt
import datetime
import secrets
from functools import wraps

SECRET_KEY = secrets.token_hex(32)


def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def auth_required(f):
    @wraps(f)
    def decorated(req, resp, *args, **kwargs):
        auth_header = req.headers.get("Authorization")

        if not auth_header or "Bearer " not in auth_header:
            resp.status_code = 401
            resp.json = {"error": "Token Required!"}
            return

        try:
            token = auth_header.split("Bearer ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            req.user_id = payload['user_id']
        except AttributeError:
            resp.status_code = 401
            resp.json = {"error": "Incorrect Token!"}
            return
        except jwt.ExpiredSignatureError:
            resp.status_code = 401
            resp.json = {"error": "Token Expired!"}
            return
        except jwt.InvalidTokenError:
            resp.status_code = 401
            resp.json = {"error": "Invalid Token"}
            return

        return f(req, resp, *args, **kwargs)

    return decorated
