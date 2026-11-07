import os
from dotenv import load_dotenv
load_dotenv()

import httpx 


from fastapi import FastAPI, HTTPException
from src.threats import router as notification_missile_router
from src.alerts import router as notification_alert_router

API_URL = os.getenv("URL1")
API_URL2 = os.getenv("URL2")

app = FastAPI()

app.include_router(notification_missile_router)
app.include_router(notification_alert_router)


@app.get("/")
async def root():
    return {
        "top" : "app"
    }
@app.get("/get_air_alert4")
async def get_air_alert():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(API_URL)
            response.raise_for_status()
        return {"active_alerts" : response.json()}
    except httpx.HTTPError:
        raise HTTPException(status_code=502)
@app.get("/get_air_threat")
async def get_air_threat():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(API_URL2)
            response.raise_for_status()
        return {"active_alerts" : response.json()}
    except httpx.HTTPError:
        raise HTTPException(status_code=502)