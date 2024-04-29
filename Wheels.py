import math

from Geometry import Point, TurnDir, Vector

class Wheels:
    def __init__(self, max_angle):
        self.max_angle = max_angle
        self.max_left_direction = Point(1, 0)
        self.max_left_direction.rotate_over_point(Point(0, 0), max_angle, TurnDir.LEFT)
        self.max_right_direction = Point(1, 0)
        self.max_right_direction.rotate_over_point(Point(0, 0), max_angle, TurnDir.RIGHT)
        self.direction = Vector(1, 0)

    def which_side_turn(self):
        if self.direction.y < 0:
            return TurnDir.RIGHT
        elif self.direction.y > 0:
            return TurnDir.LEFT
        else:
            return TurnDir.STRAIGHT

    def are_straight(self):
        return self.which_side_turn() == TurnDir.STRAIGHT

    def make_straight(self):
        self.direction.x = 1
        self.direction.y = 0

    def sin_cur_angle(self):
        return min(abs(self.direction.y), 1)
    
    def cos_cur_angle(self):
        return min(self.direction.x, 1)

    def is_max_angle(self):
        return self.direction.compare(self.max_right_direction) or self.direction.compare(self.max_left_direction)

    def cur_wheel_angle(self):
        return math.acos(self.cos_cur_angle())
        
    def turn(self, angle, dir):
        self.direction.rotate_over_point(Point(0, 0), angle, dir)
        if self.direction.y > self.max_left_direction.y:
            self.direction.copy_coordinates_from(self.max_left_direction)
        elif self.direction.y < self.max_right_direction.y:
            self.direction.copy_coordinates_from(self.max_right_direction)
        self.direction.normalize(False)