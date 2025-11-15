import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # where session.py is
SSL_CERT = os.path.join(BASE_DIR, "..", "creds", "isrgrootx1.pem")
SSL_CERT = os.path.abspath(SSL_CERT)
print(SSL_CERT)
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("SQLALCHEMY_DATABASE_URL environment variable is not set")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
     pool_pre_ping=True,       # tests connection before using it
    pool_recycle=1800,        # recycle connections every 30 minutes
    pool_size=10,             # optional: max connections in pool
    max_overflow=20,
    connect_args={
        "ssl_ca": SSL_CERT,
    },
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency to get database session
def get_db():
    print("Creating new database session")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
