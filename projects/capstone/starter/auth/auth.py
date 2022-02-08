import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import traceback
import urllib


#AUTH0_DOMAIN = 'dev-c44vwyk3.auth0.com'
AUTH0_DOMAIN = "dev-c44vwyk3.us.auth0.com"
ALGORITHMS = ['RS256']
API_AUDIENCE = 'http://127.0.0.1:5000/'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():

    
    if 'Authorization' not in request.headers :
        raise AuthError({'code': 'missing authorization', 'description': 'Authorization not in request header'}, 401)
    auth_header= request.headers['Authorization']
    header_parts= auth_header.split(' ')
    
    if len(header_parts) != 2 or not header_parts:
        raise AuthError({'code': 'missing part', 'description': 'Header parts not equal to 2'}, 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError({'code': 'invalid method', 'description': 'auth method is not bearer'}, 401)

    return(header_parts[1])

   #raise Exception('Not Implemented')


def check_permissions(permission, payload):


    if 'permissions' not in payload:
    
        abort(400)

    if permission not in payload['permissions']:

        abort(401)
    return True
    #raise Exception('Not Implemented')

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
# reference : https://github.com/udacity/FSND/blob/master/BasicFlaskAuth/app.py
def verify_decode_jwt(token):

    #raise Exception('Not Implemented')
    jsonurl = "https://{}/.well-known/jwks.json".format(AUTH0_DOMAIN)
    response = urllib.request.urlopen(jsonurl)
    jwks = json.loads(response.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:

        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:

        if key['kid'] == unverified_header['kid']:

            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:

            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
              token = get_token_auth_header()
              payload = verify_decode_jwt(token)
              check_permissions(permission, payload)
            except AuthError as authError:
                raise abort(authError.status_code,authError.error["description"])
                traceback.print_exc()
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator