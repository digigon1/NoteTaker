import datetime

import jwt
from jwt.utils import get_int_from_datetime

class JWT:
    __instance = jwt.JWT()

    @classmethod
    def init(cls, config):
        with open(config.get('jwt.private'), 'rb') as f:
            JWT.signing_key = jwt.jwk_from_pem(f.read())
        
        with open(config.get('jwt.public'), 'rb') as f:
            JWT.verifying_key = jwt.jwk_from_pem(f.read())
    
    @classmethod
    def encode(cls, user: str):
        return JWT.__instance.encode({
            'user': user,
            'iat': get_int_from_datetime(datetime.datetime.now())
        }, JWT.signing_key, alg='RS256')

    @classmethod
    def decode(cls, token: str):
        try:
            return JWT.__instance.decode(token, JWT.verifying_key)['user']
        except Exception as e:
            print(e)
            return None
