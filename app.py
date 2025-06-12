import streamlit as st
from dotenv import load_dotenv
import json
import os
import folium
from streamlit_folium import st_folium
from agents.connectivity_agent import connectivity_agent
from agents.personalization_agent import personalization_agent
from agents.layout_agent import layout_agent
from agents.crew_alert_agent import crew_alert_agent
from agents.turbulence_alert_agent import check_turbulence_alert

# Load env vars
load_dotenv()

# File paths
starlink_log_path = "data/starlink_logs.json"
profile_path = "data/passenger_profiles.json"
manifest_path = "data/passenger_manifest.json"

st.set_page_config(layout="wide", page_title="Starlink Optimizer AI Crew Panel")

st.title("✈️ AI Crew Panel - Starlink Optimizer")

# Initialize session states
if "connectivity" not in st.session_state:
    st.session_state.connectivity = None
if "personalization" not in st.session_state:
    st.session_state.personalization = None
if "layout" not in st.session_state:
    st.session_state.layout = None
if "crew" not in st.session_state:
    st.session_state.crew = None
if "taf_alert" not in st.session_state:
    st.session_state.taf_alert = None

# ========== STEP 1 ==========
if st.button("📡 Check Connectivity"):
    with st.spinner("Analyzing Starlink Logs..."):
        output = connectivity_agent.invoke({
            "input": f"Check connectivity issues in {starlink_log_path}"
        })
        st.session_state.connectivity = output["output"]
        st.success("✅ Connectivity report generated.")

if st.session_state.connectivity:
    with st.expander("📶 Connectivity Report"):
        st.write(st.session_state.connectivity)

# ========== STEP 2 ==========
if st.button("🎬 Personalize Passenger Experience"):
    if st.session_state.connectivity:
        with st.spinner("Generating personalization based on connectivity..."):
            output = personalization_agent.invoke({
                "input": f"Suggest entertainment and services using {profile_path}\nConnectivity:\n{st.session_state.connectivity}"
            })
            st.session_state.personalization = output["output"]
            st.success("✅ Personalization suggestions ready.")
    else:
        st.error("❌ Please run connectivity analysis first.")

if st.session_state.personalization:
    with st.expander("🎥 Personalization Suggestions"):
        st.write(st.session_state.personalization)

# ========== STEP 3 ==========
if st.button("🛋️ Suggest Qsuite Layout"):
    if st.session_state.personalization:
        with st.spinner("Recommending Qsuite layout..."):
            output = layout_agent.invoke({
                "input": f"Suggest best Qsuite layout using {manifest_path}\nPersonalization:\n{st.session_state.personalization}"
            })
            st.session_state.layout = output["output"]
            st.success("✅ Layout suggestion generated.")
    else:
        st.error("❌ Run personalization first.")

if st.session_state.layout:
    with st.expander("🛏️ Qsuite Layout Plan"):
        st.write(st.session_state.layout)

# ========== STEP 4 ==========
if st.button("🛎️ Final Crew Briefing"):
    if all([st.session_state.connectivity, st.session_state.personalization, st.session_state.layout]):
        with st.spinner("Generating final briefing..."):
            output = crew_alert_agent.invoke({
                "input": f"Create final briefing.\nConnectivity: {st.session_state.connectivity}\nPersonalization: {st.session_state.personalization}\nLayout: {st.session_state.layout}"
            })
            st.session_state.crew = output["output"]
            st.success("✅ Final crew briefing ready.")
    else:
        st.error("❌ Complete all previous steps first.")

if st.session_state.crew:
    with st.expander("🧾 Final Crew Briefing"):
        st.write(st.session_state.crew)

# ========== STEP 5: TAF Turbulence Alert ==========

st.subheader("🌩️ TAF Turbulence Alert")

route = st.text_input("Enter route (e.g., JFK-LHR):", value="JFK-LHR")

if st.button("🌐 Check Turbulence Alert"):
    if route:
        with st.spinner("Fetching TAF and analyzing for turbulence..."):
            result = check_turbulence_alert.invoke({"route": route})
            alerts = result.get("alerts", [])
            coords = result.get("coordinates", [])


            st.session_state.taf_alert = alerts
            st.session_state.taf_coords = coords
    else:
        st.error("❌ Please enter a valid route.")

if st.session_state.get("taf_alert"):
    for a in st.session_state.taf_alert:
        if "⚠️" in a:
            st.warning(a)
        else:
            st.success(a)

# ========== TAF MAP VISUALIZATION ==========

# Beautified TAF Alert Display
if st.session_state.get("taf_alert"):
    st.subheader("📡 Weather Summary for Route")
    
    for i, alert in enumerate(st.session_state.taf_alert):
        try:
            # Extract ICAO and weather content
            icao, info = alert.replace("⚠️", "").split(":", 1)
            icao = icao.strip()
            info = info.strip()

            if "no severe weather" in info.lower():
                st.success(f"🟢 **{icao}**: No significant weather or turbulence issues detected.")
            else:
                # Add visual tags (optional enhancement)
                tags = ""
                if "turbulence" in info.lower(): tags += "💨 "
                if "thunderstorm" in info.lower(): tags += "⛈️ "
                if "wind shear" in info.lower(): tags += "🌬️ "
                if "gust" in info.lower(): tags += "🌪️ "

                st.warning(f"🟡 **{icao}**: {tags}**{info}**")
        except Exception as e:
            st.error(f"⚠️ Could not parse alert: `{alert}`")


    dep, arr = st.session_state.taf_coords
    center_lat = (dep["lat"] + arr["lat"]) / 2
    center_lon = (dep["lon"] + arr["lon"]) / 2

    taf_map = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    folium.Marker(
        [dep["lat"], dep["lon"]],
        tooltip=f"Departure: {dep['icao']}",
        icon=folium.Icon(color="red" if "⚠️" in st.session_state.taf_alert[0] else "green")
    ).add_to(taf_map)

    folium.Marker(
        [arr["lat"], arr["lon"]],
        tooltip=f"Arrival: {arr['icao']}",
        icon=folium.Icon(color="red" if "⚠️" in st.session_state.taf_alert[1] else "green")
    ).add_to(taf_map)

    folium.PolyLine(
        [[dep["lat"], dep["lon"]], [arr["lat"], arr["lon"]]],
        color="blue", weight=2.5
    ).add_to(taf_map)

    st_folium(taf_map, width=800, height=500)
