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
async def get_air_alert():
    global alert

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(API_URL)
            response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(status_code=502)
    data = response.json()
    target_raion = "Красноградський район"
    raion = next(
        (r for r in data["raions"] if r["name"] == target_raion),
        None
    )
    if raion is None:
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

        else:
            alert_notification(
                "🟡 Повітряна тривога!",
                "У Красноградському районі оголошено жовтий рівень!",
                f"--icon={ICON}",
                "--app-name=Potushno"
            )

    elif raion["level"] not in ("red", "yellow") and alert:

        alert = False

        alert_notification(
            "🟢 Відбій повітряної тривоги!",
            "Слідкуйте за подальшими повідомленнями!",
            f"--icon={ICON}",
            "--app-name=Potushno"
        )

    return {"alert": alert}

