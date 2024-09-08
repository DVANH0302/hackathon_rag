from sqlalchemy.orm import sessionmaker, declarative_base
import os
from sqlalchemy import create_engine, text
from sqlalchemy import make_url
from .config import DATABASE_URL, DB_HOST,DB_NAME,DB_PASSWORD,DB_PORT, DB_USERNAME

Base = declarative_base()



# #### TEST
# import os 
# from dotenv import load_dotenv
# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")
# DB_USERNAME = os.getenv('DB_USERNAME')  
# DB_PASSWORD = os.getenv('DB_PASSWORD')  
# DB_HOST = os.getenv('DB_HOST')  
# DB_PORT = os.getenv('DB_PORT')  
# DB_NAME = os.getenv('DB_NAME') 
# ####

def create_engine_and_session(URL):
    engine = create_engine(URL)
    SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind = engine)
    return engine, SessionLocal



engine, SessionLocal = create_engine_and_session(DATABASE_URL)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Initialize PGVectorStore





# url = make_url(DATABASE_URL)

# def test_connection():
#     # create a connectio
#     # with engine.connect() as connection:
#     #     # execute a simple query to test the connection
#     #     result = connection.execute(text("select 1"))
#     #     print(result.fetchone())
#     pass



# if __name__ == "__main__":
#     test_connection()