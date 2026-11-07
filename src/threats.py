import os

from fastapi import APIRouter, HTTPException

import httpx

from src.notifications import missile_near_notification
router = APIRouter()

from pathlib import Path

API_URL2 = os.getenv("URL2")

ICON = Path(__file__).resolve().parent / "logo.jpg"

@router.get("/notification_threats")
async def not_thearts(
    user_lat: str,
    user_lon: str
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
        #lat = threat.get("lat")
        #lon = threat.get("lon")
        threat_type = threat.get("type")
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
        threat_type = "Невідома ціль!"
    elif threat_type == "fpv":
        threat_type == "Фпв-дрон"
    missile_near_notification("🚀 Увага ціль!", f"{threat_type} навколо вас!", f"--icon={ICON}", "--app-name=Potushno")
    return {"notification" : "sent"}
