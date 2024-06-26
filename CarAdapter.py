import Car
from Geometry import Point, Rectangle, TurnDir, Vector

class CarAdapter(Car.Car):
    """Class makes the control over the Car natural for pygame screen's coordinate system"""

    def __init__(self, width, length, front_left_pos, direction, wheels_max_turn, *, color):
        direction.y *= -1
        super().__init__(width, length, front_left_pos, direction, wheels_max_turn, color=color)
        
        width_vec = Vector(Point(0, 0), self.direction).orthogonal_vector(self.width, TurnDir.LEFT)
        front_left_pos.add_vector(width_vec, False)
        self.rect = Rectangle(front_left_pos, width, length, self.direction)
    
    def turn_left(self):
        self.wheels.turn(self.turning_speed, TurnDir.RIGHT)

    def turn_right(self):
        self.wheels.turn(self.turning_speed, TurnDir.LEFT)

    def straighten_wheels(self):
        if self.cur_turn_side() == TurnDir.RIGHT:
            self.turn_right()
            if not self.cur_turn_side() == TurnDir.RIGHT:
                self.wheels.make_straight()
        else:
            self.turn_left()
            if self.cur_turn_side() == TurnDir.RIGHT:
                self.wheels.make_straight()


    @property
    def front_left(self):
        return self.rect.front_right
    
    @property
    def front_right(self):
        return self.rect.front_left
    
    @property
    def rear_left(self):
        return self.rect.rear_right
    
    @property
    def rear_right(self):
        return self.rect.rear_left