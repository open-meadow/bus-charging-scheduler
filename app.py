import streamlit as st
import pandas as pd

from scenario_loader import SCENARIOS
from constants import SPEED, SEGMENTS, STATIONS


def to_minutes(time_string):
    hours, minutes = map(int, time_string.split(":"))
    return hours * 60 + minutes


def get_selected_buses():
    scenario_name = st.selectbox(
        "Pick scenario",
        list(SCENARIOS.keys())
    )

    return SCENARIOS[scenario_name]

def generate_schedule(buses):
    schedule = []

    for bus in buses:
        current_time = to_minutes(bus["departure"])

        schedule.append({
            "bus_id": bus["id"],
            "event": "DEPART",
            "time": current_time,
            "location": "Bengaluru"
        })

        for index, distance in enumerate(SEGMENTS):
            travel_time = int((distance / SPEED) * 60)
            current_time += travel_time

            if index < len(STATIONS):
                location = STATIONS[index]
            else:
                location = "Kochi"

            schedule.append({
                "bus_id": bus["id"],
                "event": "ARRIVE",
                "time": current_time,
                "location": location
            })

    return schedule

def render_station_view(schedule):
    st.subheader("Station View")

    for station in STATIONS:
        st.markdown(f"### Station {station}")

        arrivals = [
            event
            for event in schedule
            if event["event"] == "ARRIVE"
            and event["location"] == station
        ]

        arrivals.sort(key=lambda event: event["time"])

        if arrivals:
            st.dataframe(pd.DataFrame(arrivals))
        else:
            st.write("No arrivals")


def main():
    st.title("🚌 Bus Charging Scheduler")

    buses = get_selected_buses()

    st.subheader("Input Buses")
    st.dataframe(pd.DataFrame(buses))

    schedule = generate_schedule(buses)

    st.subheader("Generated Schedule")
    st.dataframe(pd.DataFrame(schedule))

    render_station_view(schedule)


if __name__ == "__main__":
    main()