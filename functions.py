import base64

def encrypt_password(raw_password):
    encrypted_password = raw_password.encode("ascii")
    base64_bytes = base64.b64encode(encrypted_password)
    password = base64_bytes.decode("ascii")
    return password