from typing import List, Tuple, TypedDict
from functools import reduce
from elevator import Elevator
from enums import Direction, ElevatorEvent, FloorEvent
from floor import Floor


class ElevatorWaitingQueue(TypedDict):
    floor: int
    direction: Direction


def add_floor_on_elevator_queue(
    elevator: Elevator, floor: int, direction: Direction
) -> None:
    elevator.add_floor_to_queue(floor, direction)


class Controller:
    elevators: List[Elevator]
    floors: List[Floor]
    elevator_waiting_queue: List[ElevatorWaitingQueue] = []

    def __init__(self, elevators: List[Elevator], floors: List[Floor]) -> None:
        self.elevators = elevators
        self.floors = floors

        self.init_all_subscriptions()

    def init_all_subscriptions(self) -> None:
        for elevator in self.elevators:
            self.init_elevator_subscriptions(elevator)

        for floor in self.floors:
            self.init_floor_subscriptions(floor)

    def init_elevator_subscriptions(self, elevator: Elevator) -> None:
        elevator.subscribe(
            ElevatorEvent.ELEVATOR_IS_IDLE, lambda x: print(self.elevator_waiting_queue)
        )
        elevator.subscribe(
            ElevatorEvent.ELEVATOR_REACHED_THE_DESTINATION,
            lambda elevator: self.notify_floors_about_elevator_arrival(elevator),
        )

    def init_floor_subscriptions(self, floor: Floor) -> None:
        floor.subscribe(
            FloorEvent.UP_BUTTON_PRESSED_FROM_FLOOR,
            lambda elevator_calling_floor: self.assign_elevators_to_floor(
                Direction.UP, elevator_calling_floor
            ),
        )
        floor.subscribe(
            FloorEvent.DOWN_BUTTON_PRESSED_FROM_FLOOR,
            lambda elevator_calling_floor: self.assign_elevators_to_floor(
                Direction.DOWN, elevator_calling_floor
            ),
        )

    def notify_floors_about_elevator_arrival(self, elevators: Tuple[Elevator]) -> None:
        (elevator,) = elevators

        for floor in self.floors:
            floor.publish(FloorEvent.ELEVATOR_AVAILABLE_FOR_TRANSPORT, elevator)

    def assign_elevators_to_floor(
        self, direction: Direction, elevator_calling_floor: Tuple[int]
    ) -> None:
        (floor,) = elevator_calling_floor

        elevators_on_idle_or_same_direction = (
            self.get_elevators_on_idle_or_same_direction(direction, floor)
        )

        if len(elevators_on_idle_or_same_direction) > 0:
            self.allocate_elevator_to_floor(
                elevators_on_idle_or_same_direction, floor, direction
            )
        else:
            self.add_to_elevator_waiting_queue(floor, direction)

    def allocate_elevator_to_floor(
        self, elevators: List[Elevator], floor: int, direction: Direction
    ) -> None:
        closest_elevator = self.get_closest_elevator(elevators, floor)
        add_floor_on_elevator_queue(closest_elevator, floor, direction)

    def add_to_elevator_waiting_queue(self, floor: int, direction: Direction) -> None:
        self.elevator_waiting_queue.append({"floor": floor, "direction": direction})

    def get_elevators_on_idle_or_same_direction(
        self, direction: Direction, floor: int
    ) -> List[Elevator]:
        elevators = self.get_elevator_list()
        return list(
            filter(
                lambda elevator: elevator.is_elevator_idle()
                or (
                    elevator.get_elevator_current_direction() == direction
                    and elevator.get_current_floor() < floor
                ),
                elevators,
            )
        )

    def get_closest_elevator(
        self, elevators: List[Elevator], elevator_calling_floor: int
    ) -> Elevator:
        def get_elevators(acc: Elevator, curr: Elevator):
            x = abs(curr.get_current_floor() - elevator_calling_floor)
            y = abs(acc.get_current_floor() - elevator_calling_floor)

            return curr if x < y else acc

        return reduce(get_elevators, elevators)

    def get_elevator_list(self) -> List[Elevator]:
        return self.elevators
