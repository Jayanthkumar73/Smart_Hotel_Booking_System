from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker,declarative_base

from dotenv import load_dotenv
import os 



load_dotenv()

DB_USER=os.getenv("DB_USER","root")
DB_PASSWORD=os.getenv("DB_PASSWORD","1234")
DB_HOST=os.getenv("DB_HOST","localhost")
DB_NAME=os.getenv("DB_NAME","hotel_booking_system")

DATABASE_URL=f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


engine=create_engine(DATABASE_URL)

SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)
Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


