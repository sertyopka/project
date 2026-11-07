import os

from fastapi import APIRouter, HTTPException

import httpx

from src.notifications import alert_notification
router = APIRouter()

from pathlib import Path

API_URL = os.getenv("URL3")

ICON = Path(__file__).resolve().parent / "logo.jpg"

@router.get("/get_air_alert")
async def get_air_alert():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(API_URL)
            response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(status_code=502)
    data = response.json()
    for raion in data["raions"]:
        if raion["name"] == "Конотопський район":
            if raion["level"] == "red":
                alert_notification("🔴 Повітряна тривога!", "У Вінницькому районі оголошено червоний рівень!", f"--icon={ICON}", "--app-name=Potushno")
            else:
                alert_notification("🟡 Повітряна тривога!", "У Вінницькому районі оголошено жовтий рівень!", f"--icon={ICON}", "--app-name=Potushno")
            return {"Тривогз" : "no"}
    return {"not" : "sent"}

