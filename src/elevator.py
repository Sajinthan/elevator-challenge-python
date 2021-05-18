from typing import List, Set
from enums import Direction, ElevatorEvent
from observable import Observable
from passenger import Passenger


class Elevator(Observable):
    elevator_number: int
    capacity: int
    current_floor = 0
    destination_floors: List[int] = []
    elevator_direction = Direction.IDLE
    position_y = 0
    is_idle = True
    is_moving = False
    is_waiting_for_passengers = False
    is_going_up = False
    passengers = Set[Passenger]

    def __init__(self, elevator_number: int, capacity: int) -> None:
        super().__init__
        self.elevator_number = elevator_number
        self.capacity = capacity

    def update_elevator_position(self) -> None:
        if self.position_y and self.position_y % 5 == 0:
            print("elevator {}", self.elevator_number)
            print("moving: {}", self.is_elevator_ready_to_move())
            print("position: {}", self.position_y)
            print("direction: {}", self.elevator_direction)
            print("current floor: {}", self.current_floor)
            print("destination queue: {}", self.destination_floors)
            print("---------------------------------------------------")

        if self.is_elevator_ready_to_move():
            if self.is_elevator_reached_destination():
                self.put_elevator_on_hold_if_reached_destination()
            else:
                self.set_elevator_movement()
                self.update_elevator_current_floor()
        else:
            self.notify_if_elevator_idle()

    def notify_if_elevator_idle(self) -> None:
        if (
            len(self.destination_floors) == 0
            and self.elevator_direction != Direction.IDLE
        ):
            self.elevator_direction = Direction.IDLE
            self.publish(ElevatorEvent.ELEVATOR_IS_IDLE)

    def put_elevator_on_hold_if_reached_destination(self) -> None:
        self.is_moving = False
        self.is_waiting_for_passengers = True
        self.destination_floors.pop(0)
        self.remove_passengers()
        self.publish(ElevatorEvent.ELEVATOR_REACHED_THE_DESTINATION, self)

    def remove_passengers(self) -> None:
        for passenger in self.passengers:
            if passenger.get_destination_floor() == self.current_floor:
                self.passengers.remove(passenger)

    def set_elevator_movement(self) -> None:
        if self.is_going_up:
            self.position_y += 1
        else:
            self.position_y -= 1

        self.is_idle = False
        self.is_moving = True

        [first_reaching_floor] = self.destination_floors

        if first_reaching_floor > self.current_floor:
            self.is_going_up = True
        else:
            self.is_going_up = False

    def update_elevator_current_floor(self) -> None:
        if self.position_y % 10 == 0 and self.elevator_direction != Direction.IDLE:
            if self.is_going_up:
                self.current_floor += 1
            else:
                self.current_floor -= 1

    def is_elevator_reached_destination(self) -> bool:
        [first_destination_floor] = self.destination_floors

        if self.current_floor == first_destination_floor:
            return True

        return False

    def get_elevator_current_direction(self) -> Direction:
        return self.elevator_direction

    def add_floor_to_queue(self, destination_floor: int, direction: Direction) -> None:
        self.destination_floors.append(destination_floor)
        self.set_elevator_direction(direction)

    def set_elevator_direction(self, direction: Direction):
        if self.elevator_direction == Direction.IDLE:
            self.elevator_direction = direction

        self.sort_destination_queue_by_direction()

    def is_elevator_idle(self) -> bool:
        return self.is_idle

    def get_current_floor(self) -> int:
        return self.current_floor

    def get_elevator_number(self) -> int:
        return self.elevator_number

    def get_elevator_destination_list(self) -> List[int]:
        return self.destination_floors

    def get_elevator_capacity(self) -> int:
        return self.capacity

    def get_elevator_available_space(self) -> int:
        return self.capacity - self.passengers.size

    def is_elevator_ready_to_move(self) -> bool:
        return (
            self.is_waiting_for_passengers is False
            and len(self.destination_floors) > 0
            or self.is_moving
        )

    def get_elevator_position(self) -> int:
        return self.position_y

    def add_passengers_to_elevator(self, passenger: Passenger) -> None:
        destination_floor = passenger.get_destination_floor()
        filtered_destination_floors = list(
            filter(lambda x: x == destination_floor, self.destination_floors)
        )

        if len(filtered_destination_floors) == 0:
            self.destination_floors.append(destination_floor)
            self.sort_destination_queue_by_direction()
            self.passengers.add(passenger)

    def update_waiting_for_passenger_status(self, is_waiting: bool) -> None:
        self.is_waiting_for_passengers = is_waiting

    def sort_destination_queue_by_direction(self) -> None:
        if self.elevator_direction == Direction.UP:
            self.destination_floors.sort()
        elif self.elevator_direction == Direction.DOWN:
            self.destination_floors.sort(reverse=True)
