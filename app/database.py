from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# import asyncio
# from sqlalchemy.ext.asyncio import create_async_engine



load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# engine = create_async_engine(
#    "postgresql+asyncpg://scott:tiger@localhost/test",
#     echo=True,
# )
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def test_connection():
    # Create a connection
    with engine.connect() as connection:
        # Execute a simple query to test the connection
        result = connection.execute(text("SELECT 1"))
        print(result.fetchone())

# if __name__ == "__main__":
#     test_connection()