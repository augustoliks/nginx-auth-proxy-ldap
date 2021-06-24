from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os
import json
import base64
from typing import (
    Tuple,
    Text
)


if os.getenv('ENVIRONMENT') == 'production':
    key = os.environ['SECRET_KEY']
else:
    key = b'secret key development'.zfill(32)


def encrypt(seal: str) -> str:
    cipher = AES.new(key, AES.MODE_CBC)

    cipher_text = cipher.encrypt(pad(seal.encode('utf-8'), AES.block_size))

    iv_b64 = base64.b64encode(cipher.iv).decode('utf-8')
    cipher_text_b64 = base64.b64encode(cipher_text).decode('utf-8')

    result = json.dumps({'iv': iv_b64, 'cipher_text': cipher_text_b64})

    return result


def decrypt(value: str) -> str:
    json_content = json.loads(value)

    iv_decode_b64 = base64.b64decode(json_content['iv'])
    cipher_text_decode_b64 = base64.b64decode(json_content['cipher_text'])

    cipher = AES.new(key, AES.MODE_CBC, iv_decode_b64)
    seal = unpad(cipher.decrypt(cipher_text_decode_b64), AES.block_size)

    return seal.decode('utf-8')


def seal_auth_b64(username: str, passwd: str) -> str:
    return base64.b64encode(f'{username}:{passwd}'.encode()).decode()


def unseal_auth_b64(auth_b64_seal: str) -> Tuple[Text, Text]:
    seal = base64.b64decode(auth_b64_seal.encode('utf-8'))
    username, password = seal.decode('utf-8').split(':')
    return username, password
