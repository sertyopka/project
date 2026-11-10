import os

from fastapi import APIRouter, HTTPException

import httpx

from src.notifications import missile_near_notification
from src.mathformul import haversine
router = APIRouter()

from pathlib import Path

API_URL2 = os.getenv("URL2")

ICON = Path(__file__).resolve().parent / "logo.jpg"

@router.get("/notification_threats")
async def not_thearts(
    user_lat: float,
    user_lon: float
):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(API_URL2)
            response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(status_code=502)
    data = response.json()

    threats = data.get("threats", [])

    for threat in threats:
        missile_lat = threat.get("lat")
        missile_lon = threat.get("lon")
        threat_type = threat.get("type")
        distance = haversine(user_lat, user_lon, missile_lat, missile_lon)
        if distance <= 50:
            distance = round(distance)
            missile_near_notification("🚀 Увага ціль!", f"{threat_type} навколо вас у {distance} км!", f"--icon={ICON}", "--app-name=Potushno")
    if threat_type == "uav":
        threat_type = "БпЛА"
    elif threat_type == "recon":
        threat_type = "Роздвіник"
    elif threat_type == "missile":
        threat_type = "Ракета"
    elif threat_type == "ballistic":
        threat_type = "Балістична ракета"
    elif threat_type == "kab":
        threat_type = "КАБ"
    elif threat_type == "mig31k":
        threat_type = "Міг31к"
    elif threat_type == "unknown":
        threat_type = "Невідома ціль"
    elif threat_type == "fpv":
        threat_type = "Фпв-дрон"
    return {"notification" : "sent"}
