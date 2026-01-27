from .database import engine ,SessionLocal
from .models import *
import os

def init_db():
    if os.getenv('ENV') in ('local','test'):
        Base.metadata.create_all(bind=engine)


if __name__=="__main__":
    init_db()