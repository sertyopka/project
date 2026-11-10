import os

from fastapi import APIRouter, HTTPException

import httpx

from src.notifications import alert_notification
router = APIRouter()

from pathlib import Path

API_URL = os.getenv("URL3")

ICON = Path(__file__).resolve().parent / "logo.jpg"
alert = False

@router.get("/get_air_alert")
async def get_air_alert(target_raion: str):
    global alert

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(API_URL)
            response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(status_code=502)
    data = response.json()
    raion = next(
        (r for r in data["raions"] if r["name"] == target_raion),
        None
    )
    if raion is None and alert:

        alert = False

        alert_notification(
            "🟢 Відбій повітряної тривоги!",
            "Слідкуйте за подальшими повідомленнями!",
            f"--icon={ICON}",
            "--app-name=Potushno"
        )
        return {"Vidbiy" : "Nadislano"}

    if raion is None and not alert:
        return {"status": "raion_not_found"}

    if raion["level"] in ("red", "yellow") and not alert:
        alert = True
        if raion["level"] == "red":
            alert_notification(
                "🔴 Повітряна тривога!",
                "У Красноградському районі оголошено червоний рівень!",
                f"--icon={ICON}",
                "--app-name=Potushno"
            )

        elif raion["level"] == "yellow":
            alert_notification(
                "🟡 Повітряна тривога!",
                "У Красноградському районі оголошено жовтий рівень!",
                f"--icon={ICON}",
                "--app-name=Potushno"
            )

    return {"alert": alert}

