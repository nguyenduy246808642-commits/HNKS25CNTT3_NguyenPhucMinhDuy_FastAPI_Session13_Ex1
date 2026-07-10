from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "mysql+pymysql://root:juyjuyjuy@localhost:3306/bai1_session13_db"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()