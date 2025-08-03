from fastapi import FastAPI
from pydantic import BaseModel
import json
import uuid
import os

app = FastAPI()  # FastAPI app instance — this is key for uvicorn to run

# Define a Pydantic model for incoming tracking requests
class ProductRequest(BaseModel):
    product_name: str
    min_price: int
    max_price: int
    specs: str
    sites: list[str]
    interval_minutes: int

# Health check endpoint
@app.get("/")
def root():
    return {"message": "Myra is up and running 🚀"}

# Endpoint to receive product tracking requests
@app.post("/track")
def track_product(request: ProductRequest):
    request_id = str(uuid.uuid4())

    # Load previous requests if file exists
    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            data = json.load(f)
    else:
        data = []

    # Add new request
    request_data = {
        "id": request_id,
        "product_name": request.product_name,
        "min_price": request.min_price,
        "max_price": request.max_price,
        "specs": request.specs,
        "sites": request.sites,
        "interval_minutes": request.interval_minutes
    }
    data.append(request_data)

    # Save back to config.json
    with open(config_file, "w") as f:
        json.dump(data, f, indent=2)

    return {
        "status": "success",
        "message": f"Tracking initiated for '{request.product_name}'",
        "request_id": request_id
    }
