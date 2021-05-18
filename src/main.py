from building import Building


class Main:
    num_of_floors = 5
    elevator_capacity = 2
    num_of_elevators = 1
    execution_time_in_seconds = 10

    def execute(self) -> None:
        building = Building(
            self.num_of_floors,
            self.num_of_elevators,
            self.elevator_capacity,
            self.execution_time_in_seconds,
        )

        building.init()


main = Main()
main.execute()
