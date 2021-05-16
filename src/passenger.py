from random import random
from elevator import Elevator
from enums import Direction
from floor import Floor
from observable import Observable
from utils import generate_random_number


class Passenger(Observable):
    currentFloor: int
    destinationFloor: int
    name: str

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.current_floor = 0
        self.destination_floor = 0

    def set_current_floor(self, floor: int) -> None:
        self.current_floor = floor

    def get_passenger_name(self) -> str:
        return self.name

    def get_current_floor(self) -> int:
        return self.current_floor

    def get_destination_floor(self) -> int:
        return self.destination_floor

    def move_to_elevator(self, elevator: Elevator, floor: Floor) -> None:
        elevator_direction = elevator.get_elevator_current_direction()
        num_of_floors = floor.get_num_of_floors()
        self.destination_floor = self.calculate_passenger_destination(
            elevator_direction, num_of_floors
        )

        elevator.add_passengers_to_elevator(self)
        floor.remove_passenger(self)

    def calculate_passenger_destination(
        self, direction: Direction, num_of_floors: int
    ) -> int:
        if direction == direction.up:
            return random.randint(self.current_floor + 1, num_of_floors)
        elif direction == direction.down:
            return random.randint(0, self.current_floor - 1)

        return generate_random_number(num_of_floors, [self.current_floor])
