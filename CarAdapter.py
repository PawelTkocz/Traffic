import Car

class CarAdapter(Car.Car):
    def turn_left(self):
        self.wheels.turn(self.turning_speed, 1)

    def turn_right(self):
        self.wheels.turn(self.turning_speed, -1)