import pygame
import math

def rotate_over_point(p, rotate_point, angle, dir):
    if dir == -1:
        angle = math.pi * 2 - angle
    s = math.sin(angle)
    c = math.cos(angle)
    p[0] -= rotate_point[0]
    p[1] -= rotate_point[1]
    new_x = p[0] * c - p[1] * s
    new_y = p[0] * s + p[1] * c
    p[0] = new_x + rotate_point[0]
    p[1] = new_y + rotate_point[1]
    return p

def move_point(p, vec, vec_len):
    p[0] += vec[0]*vec_len
    p[1] += vec[1]*vec_len
    return p

class Car:
    def __init__(self, width, height, start_x, start_y):
        self.rear_left = [start_x, start_y]
        self.rear_right = [start_x+width, start_y]
        self.front_left = [start_x, start_y+height]
        self.front_right = [start_x+width, start_y+height]
        self.rotate_point = [start_x + width//2, start_y]
        self.corners = [self.rear_left, self.rear_right, self.front_right, self.front_left]
        self.direction = [0, 1]
        self.vel = 0

    def turn(self, angle, dir):
        self.corners = [rotate_over_point(p, self.rotate_point, angle, dir) for p in self.corners]
        self.direction = rotate_over_point(self.direction, (0, 0), angle, dir)

    def draw(self, screen):
        pygame.draw.polygon(screen, "black", self.corners)

    def move(self):
        self.corners = [move_point(p, self.direction, self.vel) for p in self.corners]
        self.rotate_point = move_point(self.rotate_point, self.direction, self.vel)