from dataclasses import dataclass

@dataclass
class Bus:
    id: str
    operator: str
    direction: str
    departure_time: int

@dataclass
class Station:
    name: str
    charger_count: int

@dataclass
class ChargingEvent:
    station: str
    arrival_time: int
    charge_start: int
    charge_end: int
    wait_time: int