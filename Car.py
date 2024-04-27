import CarDrafter
from CarDrafter import orthogonal_vector
from CarDrafter import add_vector_to_point
import math
import Wheels

def move_point(p, vec, vec_len):
    p[0] += vec[0]*vec_len
    p[1] += vec[1]*vec_len
    return p

class Car:
    def __init__(self, width, height, start_x, start_y, *, color):
        self.width = width
        self.height = height
        self.rear_left = [start_x, start_y]
        self.rear_right = [start_x+width, start_y]
        self.front_left = [start_x, start_y+height]
        self.front_right = [start_x+width, start_y+height]
        self.corners = [self.rear_left, self.rear_right, self.front_right, self.front_left]
        self.direction = [0, 1]
        self.wheels = Wheels.Wheels(math.pi / 4)
        self.vel = 0
        self.car_drafter = CarDrafter.CarDrafter(width, height, color)

    def turn(self, angle, dir):
        self.wheels.turn(angle, dir)

    def find_left_corners(self):
        ort_vec = orthogonal_vector(self.rear_right, self.front_right, self.width, -1, vec_len=self.height)
        add_vector_to_point(self.front_right, ort_vec, self.front_left)
        add_vector_to_point(self.rear_right, ort_vec, self.rear_left)

    def find_right_corners(self):
        ort_vec = orthogonal_vector(self.rear_left, self.front_left, self.width, 1, vec_len=self.height)
        add_vector_to_point(self.front_left, ort_vec, self.front_right)
        add_vector_to_point(self.rear_left, ort_vec, self.rear_right)

    def calcutate_cur_direction(self):
        vec = [self.front_left[0] - self.rear_left[0], self.front_left[1] - self.rear_left[1]]
        self.direction[0] = vec[0] / self.height
        self.direction[1] = vec[1] / self.height

    def draw(self, screen):
        self.car_drafter.draw(self.corners, self.wheels.cur_wheel_angle(), self.wheels.is_turn_right(), screen)

    def move(self):
        #policzyc czy to dziala tez dla ruchu w tyl
        movement_dir = self.wheels.cur_movement_direction(self.direction) 
        if self.wheels.is_turn_right():
            move_point(self.front_right, movement_dir, self.vel)
            rear_right_vel = (self.height
                              - math.sqrt(self.height**2 - self.vel**2 * self.wheels.sin_cur_angle()**2)
                              + self.vel*self.wheels.cos_cur_angle())
            move_point(self.rear_right, self.direction, rear_right_vel)
            self.find_left_corners()
        else:
            move_point(self.front_left, movement_dir, self.vel)
            rear_left_vel = (self.height
                    - math.sqrt(self.height**2 - self.vel**2 * self.wheels.sin_cur_angle()**2)
                    + self.vel*self.wheels.cos_cur_angle())
            move_point(self.rear_left, self.direction, rear_left_vel)
            self.find_right_corners()

        self.calcutate_cur_direction()