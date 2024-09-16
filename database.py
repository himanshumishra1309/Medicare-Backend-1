from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_HOSTNAME =  "dpg-cr527252ng1s73e9t6e0-a"
DATABASE_PORT = "5432"
DATABASE_NAME = "college_website_ltzw"
DATABASE_USERNAME = "devs"
DATABASE_PASSWORD = "JjOnnRFYM7YHzRSaEXkq52OmjYsj6jdA"

# SQLALCHEMY_DATABASE_URL = "postgresql://devs:JjOnnRFYM7YHzRSaEXkq52OmjYsj6jdA@dpg-cr527252ng1s73e9t6e0-a/college_website_ltzw"
#postgresql://devs:JjOnnRFYM7YHzRSaEXkq52OmjYsj6jdA@dpg-cr527252ng1s73e9t6e0-a.oregon-postgres.render.com/college_website_ltzw
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}.oregon-postgres.render.com/{DATABASE_NAME}"
)

# SQLALCHEMY_DATABASE_URL = "postgresql://devs:JjOnnRFYM7YHzRSaEXkq52OmjYsj6jdA@dpg-cr527252ng1s73e9t6e0-a/college_website_ltzw"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
