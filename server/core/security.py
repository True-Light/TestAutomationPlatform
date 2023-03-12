import base64

from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from core.config import settings
from core.logger import logger_server

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
read_private_key = RSA.import_key(
    """-----BEGIN PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAMZlFriApdO+JOIs
aFtoHCu3hVTkOQi+xcobsivOZbcEZnA4O0mwu2yBnrkQ8yN8eIoFnMFL6jdhClq7
DvWS+JtkNIUQliXLKG2nVOHgjuxMVRrGVt9Rcc6p9aEwgtookpbvQNHnBjyrXsye
fpMtBFeZo0dj9ZW5T1wd2jWY51Z3AgMBAAECgYEAs/P7kO03/QEqyXBIVCjx7IFx
UhgU16bbF0DZ8rwrLL+z/zQyKtxAlOJZyznhoJ2FZIREtFwcnZDK6JNltUBTeFxF
F6U46VyaHupoWdv/EJo/E7N+SjzhjcEmvH5CRACANap8Rw6IDDw8exyIbywnGFZx
e0hfcKE9csmFjdjQ22ECQQD7Kr2a9Yua4cv435njcdAfj7DvoACp8REywaSlPRx0
Dh+gE3Lqbxp7Ks/5KI+7R8BYxLa6XHG6sGh+tlvTjDZHAkEAyjZj+3QshXO+h0j4
cAHXz+g5Hee4NIL2vTQBWIaQ0K9z7Pnvp+O/Scskw+ExNy8wZQO/pIsnL+ZdwoMe
FVeGUQJBAKuJUjs9zd22ro7Hb5tlxKV5hnbxiOKHsJ5AoEj2BrPAXZr/DXHM9YH/
CFD7gcZ/R3+Ywc9fiZDeIE/CDc7aKMsCQG0sVmixPURDzE8QF4mphRHrx8Kck3hO
aNaX2E4qQM9amtULz9ct/93gfpX+4+puYMt47aPxuROEZYSZ88kD+zECQEgAp1eg
bL0AxPIcylZdx6HvrKP51unQKl6LFaoGIFazuuON2+rL5YcYZsAq/aHGFiWgv+HZ
VdHSGkzlxrIjZDc=
-----END PRIVATE KEY-----"""
)
this_cipher = PKCS1_v1_5.new(read_private_key)


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    根据设定的时间生成令牌
    :param subject: 要加密的对象
    :param expires_delta: 令牌时限
    :return: 加密字符串
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证两组密码
    :param plain_password: 原始密码
    :param hashed_password: 哈希密码
    :return:
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger_server.error("TA:对比密码出错")
        return False


def get_password_hash(password: str) -> str:
    """
    获取密码的哈希
    :param password: 密码
    :return:
    """
    return pwd_context.hash(password)


def decrypt_data(text: str):
    decrypt_result = this_cipher.decrypt(base64.b64decode(text), 0)
    decrypt_text = decrypt_result.decode("utf-8")
    logger_server.debug(f"TA:原始内容是{text},解密的内容是{decrypt_text}")
    return decrypt_text
