from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(plain_password):
    hashed_password = generate_password_hash(password=plain_password,
                                             method="pbkdf2:sha256",
                                             salt_length=8)
    return hashed_password


def verify_password(hashed_password, plain_password):
    return check_password_hash(pwhash=hashed_password, password=plain_password)
