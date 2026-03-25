import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

# 🔴 Safety check
if not DATABASE_URL:
    raise Exception("DATABASE_URL is missing")

# 🔁 Retry DB connection
while True:
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        print("✅ Connected to DB")
        break
    except Exception as e:
        print("⏳ Waiting for DB...", e)
        time.sleep(3)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)