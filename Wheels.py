import math

from Geometry import TurnDir

class Wheels:
    def __init__(self, max_angle):
        self.max_angle = max_angle
        self.max_left_direction = rotate_over_point([1, 0], (0, 0), max_angle, -1)
        self.max_right_direction = rotate_over_point([1, 0], (0, 0), max_angle, 1)
        self.direction = [1, 0]

    def which_side_turn(self):
        if self.direction[1] < 0:
            return TurnDir.RIGHT
        elif self.direction[1] > 0:
            return TurnDir.LEFT
        else:
            return TurnDir.STRAIGHT

    def are_straight(self):
        return self.direction == [1, 0]

    def make_straight(self):
        self.direction = [1, 0]

    def sin_cur_angle(self):
        return min(abs(self.direction[1]), 1)
    
    def cos_cur_angle(self):
        return min(self.direction[0], 1)

    def is_max_angle(self):
        return self.direction == self.max_right_direction or self.direction == self.max_left_direction

    def cur_wheel_angle(self):
        return math.acos(self.cos_cur_angle())
        
    def turn(self, angle, dir):
        dir TurnDir.RIGHT
        self.direction = rotate_over_point(self.direction, (0, 0), angle, dir)
        if self.direction[1] > self.max_left_direction[1]:
            self.direction[:] = self.max_left_direction
        elif self.direction[1] < self.max_right_direction[1]:
            self.direction[:] = self.max_right_direction
        self.direction = normalize_vector(self.direction)
