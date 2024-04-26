import pygame
import math
import Wheels

def rear_left_pos(front_left, front_right, height, rear_left):
    vec = [front_left[0] - front_right[0], front_left[1] - front_right[1]]
    orth_vec = [-1 * vec[1], vec[0]]
    orth_vec_len = Wheels.distance((0, 0), orth_vec)
    k = height / orth_vec_len
    rear_left[0] = front_left[0] + orth_vec[0] * k
    rear_left[1] = front_left[1] + orth_vec[1] * k

def rear_right_pos(front_left, front_right, height, rear_right):
    vec = [front_right[0] - front_left[0], front_right[1] - front_left[1]]
    orth_vec = [vec[1], -1 * vec[0]]
    orth_vec_len = Wheels.distance((0, 0), orth_vec)
    k = height / orth_vec_len
    rear_right[0] = front_right[0] + orth_vec[0] * k
    rear_right[1] = front_right[1] + orth_vec[1] * k

class Car:
    def __init__(self, width, height, start_x, start_y):
        self.width = width
        self.height = height
        self.rear_left = [start_x, start_y]
        self.rear_right = [start_x-width, start_y]
        self.front_left = [start_x, start_y+height]
        self.front_right = [start_x-width, start_y+height]
        self.corners = [self.rear_left, self.rear_right, self.front_right, self.front_left]
        self.direction = [0, 1]
        self.wheels = Wheels.Wheels(math.pi / 3)
        self.vel = 0

    def turn(self, angle, dir):
        self.wheels.turn(angle, dir)

    def draw(self, screen):
        pygame.draw.polygon(screen, "black", self.corners)

    def move(self):
        self.wheels.move_front_wheels(self.corners, self.vel)
        rear_left_pos(self.front_left, self.front_right, self.height, self.rear_left)
        rear_right_pos(self.front_left, self.front_right, self.height, self.rear_right)
        
