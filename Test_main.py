from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL:", DATABASE_URL)


app = FastAPI()
# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)

# Pydantic models
class Address(BaseModel):
    name: str
    latitude: float
    longitude: float

# Routes
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/addresses/", response_model=Address)
async def create_address(address: Address):
    query = "INSERT INTO addresses (name, latitude, longitude) VALUES (:name, :latitude, :longitude)"
    values = {"name": address.name, "latitude": address.latitude, "longitude": address.longitude}
    last_record_id = await database.execute(query=query, values=values)
    return {**address.dict(), "id": last_record_id}

@app.get("/addresses/")
async def get_addresses(latitude: float, longitude: float, distance: float = Query(..., ge=0)):
    query = "SELECT * FROM addresses WHERE (latitude - :latitude) ** 2 + (longitude - :longitude) ** 2 <= :distance ** 2"
    values = {"latitude": latitude, "longitude": longitude, "distance": distance}
    addresses = await database.fetch_all(query=query, values=values)
    return addresses

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
