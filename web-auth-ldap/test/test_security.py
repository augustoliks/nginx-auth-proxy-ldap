from modules import security
import base64


def test_encrypted_flow():
    user = 'carlos'
    passwd = 'neto'

    seal_source = security.seal_auth_b64(user, passwd)

    seal_encrypted = security.encrypt(seal_source)
    seal_encrypted_encode_b64 = base64.b64encode(seal_encrypted.encode())

    seal_encrypted_decode_b64 = base64.b64decode(seal_encrypted_encode_b64)
    seal_decrypted = security.decrypt(seal_encrypted_decode_b64)

    user_post_processed, passwd_post_processed = security.unseal_auth_b64(seal_decrypted)

    assert user == user_post_processed
    assert passwd == passwd_post_processed
