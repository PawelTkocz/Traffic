import Car
from CarDrafter import add_vector_to_point, orthogonal_vector

class CarAdapter(Car.Car):
    """Class makes the control over the Car natural for pygame screen's coordinate system"""

    def __init__(self, width, length, start_x, start_y, direction, *, color):
        direction[1] *= -1
        super().__init__(width, length, start_x, start_y, direction, color=color)
        
        width_vec = orthogonal_vector((0, 0), self.direction, self.width, -1, 1)
        self.front_left = add_vector_to_point([start_x, start_y], width_vec)
        self.find_starting_coordinates()
    
    def turn_left(self):
        self.wheels.turn(self.turning_speed, 1)

    def turn_right(self):
        self.wheels.turn(self.turning_speed, -1)

    def straighten_wheels(self):
        if self.is_turning_right():
            self.turn_right()
            if not self.is_turning_right():
                self.wheels.make_straight()
        else:
            self.turn_left()
            if self.is_turning_right():
                self.wheels.make_straight()

    def front_left_pos(self):
        return self.front_right[:]
    
    def front_right_pos(self):
        return self.front_left[:]
    
    def rear_left_pos(self):
        return self.rear_right[:]
    
    def rear_right_pos(self):
        return self.rear_left[:]