# agents/turbulence_alert_agent.py

from langchain.agents import tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("RAPIDAPI_KEY")
HOST = os.getenv("RAPIDAPI_HOST")  # e.g., "aerodatabox.p.rapidapi.com"

@tool
def check_turbulence_alert(route: str) -> dict:
    """
    Fetch TAF and coordinates for both airports, handling list responses.
    """
    try:
        dep, arr = route.strip().upper().split('-')
        headers = {"X-RapidAPI-Key": KEY, "X-RapidAPI-Host": HOST}

        alerts = []
        coords = []

        for code in [dep, arr]:
            # Weather endpoint
            w = requests.get(f"https://{HOST}/airports/icao/{code}/weather", headers=headers)
            w.raise_for_status()
            wd = w.json()
            if isinstance(wd, list) and wd: wd = wd[0]
            taf = wd.get("taf", "")
            keywords = ["turbulence", "wind shear", "severe", "thunderstorm", "gust"]
            found = [k for k in keywords if k in taf.lower()]
            alerts.append(f"⚠️ {code}: {', '.join(found) or 'no severe weather'}")

            # Coord endpoint
            c = requests.get(f"https://{HOST}/airports/icao/{code}", headers=headers)
            c.raise_for_status()
            cd = c.json()
            if isinstance(cd, list) and cd: cd = cd[0]
            loc = cd.get("location", {})
            coords.append({"icao": code, "lat": loc.get("lat"), "lon": loc.get("lon")})

        return {"alerts": alerts, "coordinates": coords}

    except Exception as e:
        return {"alerts": [f"❌ Error: {str(e)}"], "coordinates": []}
