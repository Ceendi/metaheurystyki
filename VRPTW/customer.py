from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    no: int
    x: float
    y: float
    demand: float
    ready_time: float
    due_date: float
    service_time: float
