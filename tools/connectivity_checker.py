from langchain_core.tools import tool
import json

@tool
def check_connectivity_issues(path: str) -> str:
    """
    Check Starlink connectivity logs for poor performance based on latency, buffering, and packet loss.
    Provide a summary of problematic seats. Takes a file path to a JSON file as input.
    """
    with open(path, 'r') as f:
        logs = json.load(f)

    problematic_seats = []

    for entry in logs:
        if entry["latency_ms"] > 500 or entry["buffering_events"] > 5 or entry["packet_loss"] > 2.0:
            problematic_seats.append(
                f"Seat {entry['seat']} - Latency: {entry['latency_ms']}ms, Buffering: {entry['buffering_events']}, Packet Loss: {entry['packet_loss']}%"
            )

    if not problematic_seats:
        return "✅ All seats have good connectivity."
    
    return "\n".join(problematic_seats)
