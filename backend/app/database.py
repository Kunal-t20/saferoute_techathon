from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


DB_PATH =r"F:\projects\techathon\backend\app\DB\db.sqlite"

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
