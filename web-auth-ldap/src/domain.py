import base64
from modules import (
    security,
    ldapauth
)


def seal_auth(username, password):
    seal_b64 = security.seal_auth_b64(username, password)
    seal_encrypted = security.encrypt(seal_b64)
    seal_encrypted_b64 = base64.b64encode(seal_encrypted.encode('utf-8'))

    return seal_encrypted_b64


def unseal_auth(auth_cookie: str):
    if not auth_cookie:
        raise RuntimeError('user not is authenticated, request without auth-cookie')

    seal_encrypted_decode_b64 = base64.b64decode(auth_cookie)
    seal_decrypted_encode_b64 = security.decrypt(seal_encrypted_decode_b64.decode('utf-8'))
    user, password = security.unseal_auth_b64(seal_decrypted_encode_b64)

    return user, password


def check_credentials_in_ldap_server(ldap_params, user, password):
    auth_handler = ldapauth.LDAPAuthHandler(ldap_params)
    auth_handler.check_credentials(user, password)
