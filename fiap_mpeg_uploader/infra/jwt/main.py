import jwt
import datetime

def generate_jwt(payload, secret, algorithm='HS256', expiration_minutes=60):
    """
        Generate a JSON Web Token (JWT).
    
        :param payload: Dict, the payload data to encode.
        :param secret: String, the secret key to sign the token.
        :param algorithm: String, the algorithm to use for encoding (default: 'HS256').
        :param expiration_minutes: Int, the number of minutes until the token expires.
        :return: String, the encoded JWT.
    """
    # Add expiration time to the payload
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    payload['exp'] = expiration_time
    
    # Generate the JWT
    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token

def decode_jwt(token, secret, algorithms=['HS256']):
    """
       Decode and verify a JSON Web Token (JWT).
    
        :param token: String, the JWT to decode.
        :param secret: String, the secret key used to sign the token.
        :param algorithms: List, the algorithms to use for decoding (default: ['HS256']).
        :return: Dict, the decoded payload.
        :raises: jwt.ExpiredSignatureError, jwt.InvalidTokenError, etc.
    """
    try:
        # Decode the JWT
        decoded_payload = jwt.decode(token.strip(), secret, algorithms=algorithms)
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise ValueError("The token has expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token.")



