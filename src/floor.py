from typing import Dict, Set, Type
from elevator import Elevator
from enums import ElevatorCallingButton, FloorEvent
from observable import Observable
from passenger import Passenger
from utils import generate_random_number


class Floor(Observable):
    passengers = Set[Passenger]
    currentFloor: int
    numOfFloors: int
    elevatorCallingButtonState: Dict[ElevatorCallingButton, bool] = {}

    def __init__(self, current_floor: int, num_of_floors: int) -> None:
        super().__init__()
        # self.elevatorCallingButtonState = {
        #     [ElevatorCallingButton.UP]: False,
        #     [ElevatorCallingButton.DOWN]: True,
        # }
        self.current_floor = current_floor
        self.num_of_floors = num_of_floors
        self.init_subscriptions()

    def init_subscriptions(self) -> None:
        self.subscribe(
            FloorEvent.ELEVATOR_AVAILABLE_FOR_TRANSPORT,
            self.elevator_available_for_transport,
        )

    def elevator_available_for_transport(self, elevator: Type[Elevator]) -> None:
        self.assign_passengers_to_elevator(elevator)
        elevator.update_waiting_for_passenger_status(False)

    def assign_passengers_to_elevator(self, elevator: Type[Elevator]) -> None:
        assigned_passenger_count = 0
        elevator_capacity = elevator.get_elevator_capacity()

        if elevator.get_current_floor() == self.current_floor:
            for passenger in self.passengers:
                if assigned_passenger_count <= elevator_capacity:
                    passenger.move_to_elevator(elevator, self)
                    assigned_passenger_count = assigned_passenger_count + 1

    def add_passenger(self, passenger: Passenger) -> None:
        passenger.set_current_floor(self.current_floor)
        self.passengers.add(passenger)
        self.press_elevator_calling_button()

    def remove_passenger(self, passenger: Passenger) -> None:
        self.passengers.remove(passenger)

    def press_elevator_calling_button(self) -> None:
        if self.current_floor == 0:
            self.update_elevator_calling_button_state(ElevatorCallingButton.UP, True)
        elif self.current_floor == self.num_of_floors:
            self.update_elevator_calling_button_state(ElevatorCallingButton.DOWN, True)
        else:
            self.press_random_button()

    def press_random_button(self) -> None:
        random_number = generate_random_number(self.num_of_floors, [self.current_floor])

        if random_number < self.current_floor:
            self.update_elevator_calling_button_state(ElevatorCallingButton.down, True)
        else:
            self.update_elevator_calling_button_state(ElevatorCallingButton.up, True)

    def update_elevator_calling_button_state(
        self, direction: ElevatorCallingButton, state: bool
    ) -> None:
        if self.elevator_calling_button_state[direction] != state:
            self.elevator_calling_button_state[direction] = state
            self.call_elevators(direction)

    def call_elevators(self, direction: ElevatorCallingButton) -> None:
        print("floor {}", self.current_floor)
        print("state: {}", self.elevator_calling_button_state)
        print("------------------------------------")

        event = (
            FloorEvent.UP_BUTTON_PRESSED_FROM_FLOOR
            if direction == ElevatorCallingButton.up
            else FloorEvent.DOWN_BUTTON_PRESSED_FROM_FLOOR
        )

        self.publish(event, self.current_floor)

    def get_num_of_floors(self) -> int:
        return self.num_of_floors
