import Car

class CarAdapter(Car.Car):
    def draw(self, screen):
        self.car_drafter.draw(self.corners, self.wheels.cur_wheel_angle(), self.wheels.is_turn_right(), screen)