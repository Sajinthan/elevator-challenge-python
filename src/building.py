from random import random
from typing import List
from controller import Controller
from floor import Floor
from passenger import Passenger
from elevator import Elevator


def create_passengers() -> Passenger:
    return Passenger("passenger - " + random.randint(100))


class Building:
    num_of_floors: int
    elevators: List[Elevator] = []
    floors: List[Floor] = []
    execution_time_in_seconds: int
    execution_time_in_ms = 0

    def __init__(
        self,
        num_of_floors: int,
        num_of_elevators: int,
        capacity: int,
        execution_time_in_seconds: int,
    ) -> None:
        self.num_of_floors = num_of_floors
        self.execution_time_in_seconds = execution_time_in_seconds

        self.assign_elevators_to_building(num_of_elevators, capacity)
        self.assign_floors_to_building(num_of_floors)

        Controller(self.elevators, self.floors)

    def init(self):
        self.execute()

    def execute(self) -> None:
        self.execution_time_in_ms += 100

        if self.execution_time_in_ms > self.execution_time_in_seconds * 1000:
            print()
        elif self.execution_time_in_ms % 1000 == 0:
            passenger = create_passengers()
            self.assign_passengers_to_floor(passenger)

        self.update_elevator_position()

    def update_elevator_position(self) -> None:
        for elevator in self.elevators:
            elevator.update_elevator_position()

    def assign_elevators_to_building(
        self, num_of_elevators: int, capacity: int
    ) -> None:
        for i in range(num_of_elevators):
            self.elevators.append(Elevator(i, capacity))

    def assign_floors_to_building(self, num_of_floors: int) -> None:
        for i in range(num_of_floors):
            self.floors.append(Floor(i, num_of_floors))

    def assign_passengers_to_floor(self, passenger: Passenger) -> None:
        random_number = random.randint(self.num_of_floors)
        floor = self.floors[random_number]
        floor.add_passenger(passenger)
