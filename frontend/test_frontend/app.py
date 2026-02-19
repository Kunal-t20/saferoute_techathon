import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

API_BASE = "http://127.0.0.1:8000"

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(page_title="Safe Route AI", layout="wide")
st.title("🚦 Safe Route AI – Demo Dashboard")

# ==================================================
# SIDEBAR CONTROLS
# ==================================================
st.sidebar.header("Route Input")

start = st.sidebar.text_input("Start Location")
end = st.sidebar.text_input("End Location")

check_route = st.sidebar.button("Check Route Risk")

st.sidebar.divider()

# ==================================================
# HAZARD REPORT
# ==================================================
st.sidebar.header("Report Hazard")

hazard_present = st.sidebar.radio("Is there a hazard?", ["No", "Yes"])

if hazard_present == "Yes":

    h_lat = st.sidebar.number_input("Latitude", value=19.07)
    h_lng = st.sidebar.number_input("Longitude", value=72.87)

    HAZARD_TYPES = {
        "Physical": ["Pothole", "Debris", "Broken Road", "Construction"],
        "Environmental": ["Fog", "Rain", "Flood", "Glare"],
        "Human": ["Reckless Driving", "Jaywalking", "Cyclist"],
        "Animal": ["Stray Dog", "Cattle", "Wildlife"],
        "Other": ["Unknown"]
    }

    category = st.sidebar.selectbox("Category", list(HAZARD_TYPES.keys()))
    hazard_type = st.sidebar.selectbox("Type", HAZARD_TYPES[category])

    if category == "Other":
        custom = st.sidebar.text_input("Describe Hazard")
        if custom.strip():
            hazard_type = custom

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
            st.sidebar.success("Hazard Reported!")
        else:
            st.sidebar.error("Failed to submit")

# ==================================================
# MAIN CONTENT
# ==================================================
st.header("🧠 Route Risk Analysis")

if check_route:

    if start.strip() == "" or end.strip() == "":
        st.warning("Please enter both start and end locations.")

    else:
        try:
            response = requests.post(
                f"{API_BASE}/route-risk",
                json={"start": start, "end": end}
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state["route_data"] = data

                c1, c2, c3 = st.columns([1, 1, 2])

                with c1:
                    st.metric("Risk %", data["risk_percentage"])

                with c2:
                    level = data["level"].upper()
                    if level == "HIGH":
                        st.error(level)
                    elif level == "MEDIUM":
                        st.warning(level)
                    else:
                        st.success(level)

                with c3:
                    st.info(data.get("explanation", "No explanation"))

            else:
                st.error("Backend API Error")

        except Exception as e:
            st.error(f"Connection Error: {e}")

st.divider()

# ==================================================
# MAP VISUALIZATION
# ==================================================
st.header("🔥 Route + Heatmap Visualization")

try:
    res = requests.get(f"{API_BASE}/heatmap")

    if res.status_code != 200:
        st.error("Heatmap API failed")

    else:
        hm = res.json()
        df = pd.DataFrame(hm["data"])

        if not df.empty:

            # ---------- RISK COLORS ----------
            def risk_color(r):
                if r == "high":
                    return [255, 0, 0]
                elif r == "medium":
                    return [255, 165, 0]
                return [0, 200, 0]

            df["color"] = df["risk"].apply(risk_color)

            # ---------- HEATMAP ----------
            heat_layer = pdk.Layer(
                "HeatmapLayer",
                data=df,
                get_position='[lng, lat]',
                get_weight='intensity',
                radiusPixels=40
            )

            # ---------- CLUSTER DOTS ----------
            cluster_layer = pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position='[lng, lat]',
                get_fill_color='color',
                get_line_color=[0, 0, 0],
                stroked=True,
                line_width_min_pixels=2,
                get_radius="intensity * 6",
                pickable=True
            )

            layers = [heat_layer, cluster_layer]

            # ---------- HAZARD MARKERS ----------
            try:
                hz = requests.get(f"{API_BASE}/hazards").json()
                haz_df = pd.DataFrame(hz)

                if not haz_df.empty:
                    hazard_layer = pdk.Layer(
                        "ScatterplotLayer",
                        data=haz_df,
                        get_position='[lng, lat]',
                        get_fill_color=[255, 0, 0],
                        get_radius=180,
                        pickable=True
                    )
                    layers.append(hazard_layer)

            except:
                pass

            # ==================================================
            # ROUTE + MARKERS
            # ==================================================
            if "route_data" in st.session_state:

                rd = st.session_state["route_data"]

                if "route_path" in rd:

                    # ---------- REAL ROUTE ----------
                    route_coords = [
                        [p["lng"], p["lat"]]
                        for p in rd["route_path"]
                    ]

                    route_data = [{"path": route_coords}]

                    route_layer = pdk.Layer(
                        "PathLayer",
                        data=route_data,
                        get_path="path",
                        get_width=8,
                        get_color=[0, 150, 255],
                        pickable=False
                    )

                    layers.append(route_layer)

                    # ---------- START / END ----------
                    markers = pd.DataFrame([
                        {
                            "name": "Start",
                            "lat": rd["start_lat"],
                            "lng": rd["start_lng"],
                            "color": [0, 255, 0]
                        },
                        {
                            "name": "End",
                            "lat": rd["end_lat"],
                            "lng": rd["end_lng"],
                            "color": [255, 0, 0]
                        }
                    ])

                    marker_layer = pdk.Layer(
                        "ScatterplotLayer",
                        data=markers,
                        get_position='[lng, lat]',
                        get_fill_color='color',
                        get_radius=200,
                        pickable=True
                    )

                    layers.append(marker_layer)

                    # center on route
                    center_lat = sum(p["lat"] for p in rd["route_path"]) / len(rd["route_path"])
                    center_lng = sum(p["lng"] for p in rd["route_path"]) / len(rd["route_path"])

                else:
                    center_lat = df["lat"].mean()
                    center_lng = df["lng"].mean()

            else:
                center_lat = df["lat"].mean()
                center_lng = df["lng"].mean()

            view_state = pdk.ViewState(
                latitude=center_lat,
                longitude=center_lng,
                zoom=11
            )

            deck = pdk.Deck(
                layers=layers,
                initial_view_state=view_state,
                tooltip={"text": "Risk: {risk}\nIntensity: {intensity}\n{name}"}
            )

            st.pydeck_chart(deck)

        else:
            st.warning("No heatmap data available")

except Exception as e:
    st.error(f"Map load error: {e}")

st.divider()

# ==================================================
# HAZARD LIST
# ==================================================
st.header("⚠ Existing Hazards")

if st.button("Load Hazards"):
    try:
        hz = requests.get(f"{API_BASE}/hazards").json()
        st.json(hz)
    except:
        st.error("Failed to load hazards")
