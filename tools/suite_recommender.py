from langchain_core.tools import tool
import json
import re
from collections import defaultdict

@tool
def suggest_qsuite_layout(path: str) -> str:
    """
    Analyzes a passenger manifest and recommends Qsuite configurations based on proximity.
    Input: path to passenger_manifest.json
    Output: recommendations for suite layout.
    """
    with open(path, 'r') as f:
        manifest = json.load(f)

    # Extract seat mappings
    seat_map = defaultdict(list)
    for passenger in manifest:
        match = re.match(r"(\d+)([A-Z])", passenger["seat"])
        if match:
            row, col = int(match.group(1)), match.group(2)
            seat_map[row].append((col, passenger["name"]))

    recommendations = []

    for row in sorted(seat_map.keys()):
        seats = sorted(seat_map[row], key=lambda x: x[0])
        if len(seats) >= 4:
            names = ', '.join(name for _, name in seats[:4])
            recommendations.append(f"👨‍👩‍👧‍👦 Recommend a **Quad Suite** in row {row} for: {names}")
        elif len(seats) == 2:
            names = ', '.join(name for _, name in seats)
            recommendations.append(f"💑 Recommend a **Couple Suite** in row {row} for: {names}")
        else:
            for _, name in seats:
                recommendations.append(f"🧍 Recommend a **Solo Suite** in row {row} for: {name}")

    return "\n".join(recommendations)
