import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

current_path=os.path.dirname(os.path.realpath(__file__))
database_url=f"sqlite:///{current_path}/database.db"

engine=create_engine(database_url,echo=True)

SessionLocal=sessionmaker(bind=engine)


