import jwt
from .constants import SECRET_KEY
import json

def generate_jwt_token(userObject):
    try:
        generated_token = jwt.encode({'username':userObject.username}, SECRET_KEY, algorithm="HS256")
        return generated_token
    except Exception as e:
        raise Exception(e)
    

