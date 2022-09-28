from os.path import join as join_path
from pathlib import Path

from passlib.context import CryptContext

BASE_DIR = Path(__file__).parent.parent
UPLOADS_DIR = join_path(BASE_DIR, 'uploads')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def encode_password(raw_password: str):
    assert raw_password, 'Password can not be null'
    return pwd_context.hash(raw_password)


def match_password(raw_password: str, encoded_password):
    assert raw_password, 'Raw password can not be null'
    assert encoded_password, 'Encoded password can not be null'
    return pwd_context.verify(raw_password, encoded_password)
