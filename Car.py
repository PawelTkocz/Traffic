import CarDrafter
from CarDrafter import orthogonal_vector
from CarDrafter import add_vector_to_point
from Wheels import normalize_vector
import math
import Wheels

def move_point(p, vec, vec_len):
    p[0] += vec[0]*vec_len
    p[1] += vec[1]*vec_len
    return p

class Car:
    """Class simulating functioning of car in Cartesian coordinate system"""
    turning_speed = 0.05
    acceleration = 0.1
    max_speed = 10
    brake_val = 0.1
    resistance = 0.03

    def __init__(self, width, length, start_x, start_y, direction, *, color):
        self.width = width
        self.length = length
        if direction[0] == 0 and direction[1] == 0:
            self.direction = [1, 0]
        else:
            self.direction = normalize_vector(direction)
        self.front_left = [start_x, start_y]
        self.find_starting_coordinates()
        self.wheels = Wheels.Wheels(math.pi / 3)
        self.vel = 0
        self.car_drafter = CarDrafter.CarDrafter(width, length, color)

    def find_starting_coordinates(self):
        width_vec = orthogonal_vector((0, 0), self.direction, self.width, 1, 1)
        self.front_right = add_vector_to_point(self.front_left, width_vec)
        length_vec = orthogonal_vector(self.front_right, self.front_left, self.length, -1, self.width)
        self.rear_left = add_vector_to_point(self.front_left, length_vec)
        self.rear_right = add_vector_to_point(self.rear_left, width_vec)
        self.corners = [self.rear_left, self.rear_right, self.front_right, self.front_left]

    def speed_up_front(self, limit=None):
        if self.vel >= 0:
            if limit is None:
                self.vel += self.acceleration
                self.vel = min(self.vel, self.max_speed)
            elif self.vel <= limit:
                self.vel += self.acceleration
                self.vel = min(self.vel, limit)
            else:
                self.brake()
                self.vel = max(self.vel, limit)

    def speed_up_reverse(self, limit=None):
        if self.vel <= 0:
            if limit is None:
                self.vel -= self.acceleration
                self.vel = max(self.vel, -1 * self.max_speed)
            elif self.vel >= limit:
                self.vel -= self.acceleration
                self.vel = max(self.vel, limit)
            else:
                self.brake()
                self.vel = min(self.vel, limit)

    def slow_down(self, vel):
        if self.vel > 0:
            self.vel -= vel
            self.vel = max(0, self.vel)
        elif self.vel < 0:
            self.vel += vel
            self.vel = min(0, self.vel)

    def brake(self):
        self.slow_down(self.brake_val)

    def turn_left(self):
        self.wheels.turn(self.turning_speed, -1)

    def turn_right(self):
        self.wheels.turn(self.turning_speed, 1)

    def is_turning_right(self):
        return self.wheels.is_turn_right()

    def straighten_wheels(self):
        if self.is_turning_right():
            self.turn_left()
            if not self.is_turning_right():
                self.wheels.make_straight()
        else:
            self.turn_right()
            if self.is_turning_right():
                self.wheels.make_straight()

    def find_left_corners(self):
        ort_vec = orthogonal_vector(self.rear_right, self.front_right, self.width, -1, vec_len=self.length)
        add_vector_to_point(self.front_right, ort_vec, self.front_left)
        add_vector_to_point(self.rear_right, ort_vec, self.rear_left)

    def find_right_corners(self):
        ort_vec = orthogonal_vector(self.rear_left, self.front_left, self.width, 1, vec_len=self.length)
        add_vector_to_point(self.front_left, ort_vec, self.front_right)
        add_vector_to_point(self.rear_left, ort_vec, self.rear_right)

    def calcutate_cur_direction(self):
        vec = [self.front_left[0] - self.rear_left[0], self.front_left[1] - self.rear_left[1]]
        self.direction = normalize_vector(vec)

    def draw(self, screen):
        self.car_drafter.draw(self.corners, self.wheels.cur_wheel_angle(), self.is_turning_right(), screen)

    def move(self):
        movement_dir = self.wheels.cur_movement_direction(self.direction) 
        if self.is_turning_right():
            move_point(self.front_right, movement_dir, self.vel)
            rear_right_vel = (self.length
                              - math.sqrt(self.length**2 - self.vel**2 * self.wheels.sin_cur_angle()**2)
                              + self.vel*self.wheels.cos_cur_angle())
            move_point(self.rear_right, self.direction, rear_right_vel)
            self.find_left_corners()
        else:
            move_point(self.front_left, movement_dir, self.vel)
            rear_left_vel = (self.length
                    - math.sqrt(self.length**2 - self.vel**2 * self.wheels.sin_cur_angle()**2)
                    + self.vel*self.wheels.cos_cur_angle())
            move_point(self.rear_left, self.direction, rear_left_vel)
            self.find_right_corners()

        self.calcutate_cur_direction()
        self.slow_down(self.resistance)