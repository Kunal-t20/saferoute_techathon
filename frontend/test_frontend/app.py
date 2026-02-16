import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Safe Route AI", layout="wide")
st.title("🚦 Safe Route AI – Test Dashboard")

# ================= ROUTE RISK =================
st.header("Route Risk Check")

start = st.sidebar.text_input("Start Location", "")
end = st.sidebar.text_input("End Location", "")

if st.sidebar.button("Check Route Risk"):
    if start.strip() == "" or end.strip() == "":
        st.warning("Please enter both locations")
    else:
        response = requests.post(
            f"{API_BASE}/route-risk",
            json={"start": start, "end": end}
        )

        if response.status_code == 200:
            data = response.json()

            c1, c2 = st.columns([1, 2])

            with c1:
                st.metric("Risk %", data["risk_percentage"])
                st.success(f"Level: {data['level'].upper()}")

            with c2:
                st.info(data.get("explanation", "No explanation available"))
        else:
            st.error("API Error")

st.divider()

# ================= HAZARD REPORT =================
st.sidebar.header("Report Hazard")

hazard_present = st.sidebar.radio(
    "Is there a hazard?",
    ["No", "Yes"]
)

if hazard_present == "Yes":

    h_lat = st.sidebar.number_input("Latitude", value=19.07)
    h_lng = st.sidebar.number_input("Longitude", value=72.87)

    HAZARD_TYPES = {
        "Physical": ["Pothole", "Debris", "Broken Road", "Construction"],
        "Environmental": ["Fog", "Rain", "Glare", "Flood"],
        "Human": ["Reckless Driving", "Jaywalking", "Cyclist"],
        "Animal": ["Stray Dog", "Cattle", "Wildlife"],
        "Other": ["Unknown"]
    }

    category = st.sidebar.selectbox(
        "Hazard Category",
        list(HAZARD_TYPES.keys())
    )

    hazard_type = st.sidebar.selectbox(
        "Hazard Type",
        HAZARD_TYPES[category]
    )

    # Custom input if Other
    if category == "Other":
        custom_type = st.sidebar.text_input("Describe Hazard")
        if custom_type.strip():
            hazard_type = custom_type

    h_desc = st.sidebar.text_input("Description")

    if st.sidebar.button("Submit Hazard"):
        payload = {
            "lat": h_lat,
            "lng": h_lng,
            "category": category,
            "type": hazard_type,
            "description": h_desc if h_desc else "No description"
        }

        res = requests.post(f"{API_BASE}/report-hazard", json=payload)

        if res.status_code == 200:
            st.success("Hazard Reported!")
        else:
            st.error("Failed to submit")

else:
    st.sidebar.info("No hazard to report ")

st.divider()

# ================= VIEW HAZARDS =================
st.header("Existing Hazards")

if st.button("Load Hazards"):
    hz = requests.get(f"{API_BASE}/hazards").json()
    st.json(hz)

st.divider()

# ================= HEATMAP MAP =================
st.header("Heatmap Visualization")

if st.button("Load Heatmap Map"):
    hm = requests.get(f"{API_BASE}/heatmap").json()

    df = pd.DataFrame(hm["data"])

    if not df.empty:
        heat_layer = pdk.Layer(
            "HeatmapLayer",
            data=df,
            get_position='[lng, lat]',
            get_weight='intensity',
            radiusPixels=60
        )

        view_state = pdk.ViewState(
            latitude=df["lat"].mean(),
            longitude=df["lng"].mean(),
            zoom=10
        )

        deck = pdk.Deck(
            layers=[heat_layer],
            initial_view_state=view_state,
            tooltip={"text": "Risk Intensity: {intensity}"}
        )

        st.pydeck_chart(deck)
    else:
        st.warning("No heatmap data available")
