from fastapi import FastAPI
import requests
from database import SessionLocal, engine
from models import Base, Customer

app = FastAPI()   # ✅ MUST be before @app

Base.metadata.create_all(bind=engine)


@app.post("/api/ingest")
def ingest():
    db = SessionLocal()

    res = requests.get("http://mock-server:5001/api/customers?page=1&limit=10").json()

    for c in res["data"]:
        customer_data = {
            "customer_id": c["customer_id"],
            "first_name": c["first_name"],
            "last_name": c["last_name"],
            "email": c["email"],
            "phone": c["phone"],
            "address": c["address"],
            "date_of_birth": c["date_of_birth"],
            "account_balance": c["account_balance"],
            "created_at": c["created_at"]
        }

        db.add(Customer(**customer_data))

    db.commit()
    return {"status": "success"}


@app.get("/api/customers")
def get_customers():
    db = SessionLocal()
    return db.query(Customer).all()