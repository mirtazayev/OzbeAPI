from uuid import uuid4
from time import time_ns
from passlib.context import CryptContext
from os.path import join as join_path
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
UPLOADS_DIR = join_path(BASE_DIR, 'uploads')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def unique_code():
    return f'{time_ns()}{uuid4()}'


def get_extension(filename: str):
    return filename.split(".")[-1]


def generate_new_name(filename: str):
    return f'{unique_code()}.{get_extension(filename)}'


def encode_password(raw_password: str):
    assert raw_password, 'Password can not be null'
    return pwd_context.hash(raw_password)


def match_password(raw_password: str, encoded_password):
    assert raw_password, 'Raw password can not be null'
    assert encoded_password, 'Encoded password can not be null'
    return pwd_context.verify(raw_password, encoded_password)
