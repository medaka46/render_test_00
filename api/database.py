
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import os

import shutil


# DATABASE_URL = "sqlite:///./test_08_db_p.db"

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# ----------

# DATABASE_URL = "sqlite:///./test_08_db_p.db"


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATABASE_PATH = os.path.join(BASE_DIR, '../test_08_db_p.db')

# # Create the database URL
# DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# # Create an engine
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# # Create a configured "Session" class
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Create a base class for the models
# Base = declarative_base()

# ----------------

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


# ----------------
# Determine the environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')

if ENVIRONMENT == 'production':
    # Path to the existing database file in your project root directory
    LOCAL_DB_PATH = os.path.join(os.path.dirname(__file__), '../test_08_db_new.db')
    # LOCAL_DB_PATH = os.path.join(os.path.dirname(__file__), '../test_08_db.db')
    # Path to the database file in the /tmp directory
    TMP_DB_PATH = '/tmp/test_08_db.db'
    # Copy the database file to /tmp if it doesn't already exist
    if not os.path.exists(TMP_DB_PATH):
        shutil.copyfile(LOCAL_DB_PATH, TMP_DB_PATH)
    DATABASE_URL = f"sqlite:///{TMP_DB_PATH}"
else:
    # Local development database path
    LOCAL_DB_PATH = os.path.join(os.path.dirname(__file__), '../test_08_db_new.db')
    # LOCAL_DB_PATH = os.path.join(os.path.dirname(__file__), '../test_08_db.db')
    DATABASE_URL = f"sqlite:///{LOCAL_DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

