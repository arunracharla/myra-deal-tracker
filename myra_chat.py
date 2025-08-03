from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
import uuid

app = FastAPI()  # <-- THIS is the important part

# Sample schema
class ProductRequest(BaseModel):
    product_name: str
    min_price: int
    max_price: int
    specs: str
    sites: list

@app.get("/")
def root():
    return {"message": "Myra is up and running 🚀"}

@app.post("/track")
def track_product(data: ProductRequest):
    request_id = str(uuid.uuid4())

    # You could save this request to a queue or config.json or DB here
    with open("requests_log.json", "a") as f:
        f.write(json.dumps({"id": request_id, **data.dict()}, indent=2) + ",\n")

    return {"status": "success", "request_id": request_id}
