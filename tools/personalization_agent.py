from langchain_core.tools import tool
import json

@tool
def suggest_personalized_experience(path: str) -> str:
    """
    Analyzes passenger profiles to suggest personalized entertainment and food/service.
    Returns suggestions based on preferences and current watch time.
    Input: path to passenger_profiles.json
    """
    with open(path, 'r') as f:
        profiles = json.load(f)

    suggestions = []

    for passenger in profiles:
        name = passenger['name']
        seat = passenger['seat']
        watch_time = passenger['watch_time']
        prefs = passenger['preferences']
        current_show = passenger.get('watching', 'Unknown')

        # Entertainment Suggestion
        if watch_time < 15:
            genre = prefs[0] if prefs else "general"
            entertainment = f"Recommend {genre} content to {name} in seat {seat} (currently watching '{current_show}' for {watch_time} mins)."
        else:
            entertainment = f"{name} in seat {seat} is engaged with '{current_show}' ({watch_time} mins) — no change needed."

        # Food/Service Suggestion
        snack_pref = next((p for p in prefs if p in ["tea", "coffee", "snacks", "hot chocolate"]), "light refreshments")
        service = f"Offer {snack_pref} to {name} at seat {seat}."

        suggestions.append(f"🎬 {entertainment}\n🍽️ {service}")

    return "\n\n".join(suggestions)
