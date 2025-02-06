from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker





DATABASE_URL = 'sqlite:///crud.db'
engine = create_engine(DATABASE_URL,echo=True)

Session = sessionmaker(autocommit=False,autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass




def get_db():
    db = Session()

    try:
        yield db
    finally:
        db.close()

