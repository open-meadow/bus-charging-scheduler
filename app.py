import streamlit as st
import pandas as pd

st.title("Bus charging scheduler")

# hard coded scenario

SCENARIOS = {
    "Scenario 1": [
        {"id": "bus-1", "operator": "kpn", "direction": "B→K", "departure": "19:00"},
        {"id": "bus-2", "operator": "flix", "direction": "K→B", "departure": "19:10"},
        {"id": "bus-3", "operator": "fresh", "direction": "B→K", "departure": "19:20"},
    ],
    "Scenario 2": [
        {"id": "bus-4", "operator": "kpn", "direction": "B→K", "departure": "19:00"},
        {"id": "bus-5", "operator": "flix", "direction": "K→B", "departure": "19:05"},
        {"id": "bus-6", "operator": "fresh", "direction": "B→K", "departure": "19:08"},
        {"id": "bus-7", "operator": "kpn", "direction": "K→B", "departure": "19:12"},
    ]
}

# select scenario

scenario_name = st.selectbox("Pick scenario", list(SCENARIOS.keys()))
buses = SCENARIOS[scenario_name]

st.subheader("Input buses")

df = pd.DataFrame(buses)
st.dataframe(df)

# sample scheduler - logic not implemented

st.subheader("fake schedule")

schedule = []

for i, bus in enumerate(buses):
    schedule.append({
        "bus_id": bus["id"],
        "event": "DEPART",
        "time": bus["departure"],
        "location": "Origin"
    })

    schedule.append({
        "bus_id": bus["id"],
        "event": "ARRIVE",
        "time": f"{19 + i}:45",
        "location": "Station B"
    })

    schedule.append({
        "bus_id": bus["id"],
        "event": "CHARGE",
        "time": f"{20 + i}:10 - {20 + i}:35",
        "location": "Station B"
    })

    schedule.append({
        "bus_id": bus["id"],
        "event": "ARRIVE",
        "time": f"{21 + i}:30",
        "location": "Destination"
    })

st.dataframe(pd.DataFrame(schedule))

# station view

st.subheader("Station view (fake)")

for station in ["A", "B", "C", "D"]:
    st.markdown(f"### Station: {station}")
    st.write("placeholder")
    st.write([bus["id"] for bus in buses])