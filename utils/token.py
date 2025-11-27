from datetime import datetime, timedelta
from jose import JWTError, jwt, ExpiredSignatureError #pip install python-jose
from typing import Optional
from variables import SECRET_KEY, ALGORITHM  

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Genera un nuevo token JWT con expiración configurable.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=140))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str, verify_exp: bool = True):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": verify_exp})
    except ExpiredSignatureError:
        raise ExpiredSignatureError
    except JWTError:
        raise JWTError