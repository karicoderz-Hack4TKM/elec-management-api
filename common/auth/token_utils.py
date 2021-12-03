from functools import wraps
from flask import current_app,request
import jwt


def verifyToken(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return {'code':401,'message':'Token is missing!'}

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'],algorithms=["HS256"])
            tokenData=data["data"]
            kwargs = dict({"userDetails":tokenData},**kwargs)

        except:
            return {'code':401,'message':'Token is invalid!'}

        return f(*args,**kwargs)

    return decorated

def verifyTokenForEmail(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return {'code':401,'message':'Token is missing!'},401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY_FOR_EMAIL'],algorithms=["HS256"])
            tokenData=data["data"]
            kwargs = dict({"userDetails":tokenData},**kwargs)

        except:
            return {'code':401,'message':'Token is invalid!'},401

        return f(*args,**kwargs)

    return decorated