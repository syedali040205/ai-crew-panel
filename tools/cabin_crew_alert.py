from langchain_core.tools import tool
import json

@tool
def generate_cabin_crew_alerts() -> str:
    """
    Generates a comprehensive cabin crew briefing using starlink logs, passenger profiles, and the manifest.
    Assumes default file paths: 
    - C:\\Users\\Syed Ayaan\\Projects\\StarlinkOptimizer\\data\\starlink_logs.json
    - C:\\Users\\Syed Ayaan\\Projects\\StarlinkOptimizer\\data\\passenger_profiles.json
    - C:\\Users\\Syed Ayaan\\Projects\\StarlinkOptimizer\\data\\passenger_manifest.json
    """

    # Load data
    with open(r"C:\Users\Syed Ayaan\Projects\StarlinkOptimizer\data\starlink_logs.json", "r") as f:
        logs = json.load(f)
    with open(r"C:\Users\Syed Ayaan\Projects\StarlinkOptimizer\data\passenger_profiles.json", "r") as f:
        profiles = json.load(f)
    with open(r"C:\Users\Syed Ayaan\Projects\StarlinkOptimizer\data\passenger_manifest.json", "r") as f:
        manifest = json.load(f)

    # Build lookup tables
    seat_to_name = {p["seat"]: p["name"] for p in manifest}
    name_to_profile = {p["name"]: p for p in profiles}

    alerts = []

    for entry in logs:
        seat = entry["seat"]
        name = seat_to_name.get(seat, "Unknown")
        profile = name_to_profile.get(name, {})

        # Basic connectivity alert
        if entry["connection_status"] in ["unstable", "intermittent"]:
            issue = f"⚠️ Passenger **{name}** (Seat {seat}) is experiencing {entry['connection_status']} connectivity.\n"
            if profile:
                issue += f"👉 Offer alternative options for **{profile.get('watching', 'unknown show')}**, or provide {', '.join(profile.get('preferences', []))}.\n"
            alerts.append(issue)

        # Flag passengers with no profile match
        if not profile:
            alerts.append(f"🔍 No profile found for {name} at seat {seat}. Consider checking manually.")

    if not alerts:
        return "✅ No critical alerts. All systems performing well."

    return "\n".join(alerts)
