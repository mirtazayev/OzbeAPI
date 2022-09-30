from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

DATABASE_URL = 'postgresql+psycopg2://postgres:1@localhost/ozbe'
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
