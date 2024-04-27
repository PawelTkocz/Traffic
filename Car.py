import pygame
import math
import Wheels

def move_point(p, vec, vec_len):
    p[0] += vec[0]*vec_len
    p[1] += vec[1]*vec_len
    return p

def orthogonal_vector(vec_b, vec_e, end_len, dir, vec_len = 0):
    #creates orthogonal vector to vec that
    #"turns" right or left depending on dir
    vec = [vec_e[0] - vec_b[0], vec_e[1] - vec_b[1]]
    
    if dir == 1: orth_vec = [vec[1], -1 * vec[0]]
    else: orth_vec = [-1* vec[1], vec[0]]

    if vec_len == 0:
        vec_len = Wheels.distance((0, 0), orth_vec)
    k = end_len / vec_len

    orth_vec[0] *= k
    orth_vec[1] *= k
    return orth_vec
    
def add_vector_to_point(p_b, vec, p_e):
    p_e[0] = p_b[0] + vec[0]
    p_e[1] = p_b[1] + vec[1]

class Car:
    def __init__(self, width, height, start_x, start_y):
        self.width = width
        self.height = height
        self.rear_left = [start_x, start_y]
        self.rear_right = [start_x+width, start_y]
        self.front_left = [start_x, start_y+height]
        self.front_right = [start_x+width, start_y+height]
        self.corners = [self.rear_left, self.rear_right, self.front_right, self.front_left]
        self.direction = [0, 1]
        self.wheels = Wheels.Wheels(math.pi / 3)
        self.vel = 0

    def turn(self, angle, dir):
        self.wheels.turn(angle, dir)

    def draw_lights(self, screen):
        light_left_pts = [[0, 0] for i in range(4)]
        light_right_pts = [[0, 0] for i in range(4)]
        height_vec = orthogonal_vector(self.front_left, self.front_right, 10, 1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, 30, 1, self.height)   
        light_left_pts[0] = self.front_left
        add_vector_to_point(self.front_left, height_vec, light_left_pts[1])
        add_vector_to_point(light_left_pts[1], width_vec, light_left_pts[2])
        add_vector_to_point(self.front_left, width_vec, light_left_pts[3])

        width_vec = orthogonal_vector(self.rear_left, self.front_left, 30, -1, self.height)   
        light_right_pts[0] = self.front_right
        add_vector_to_point(self.front_right, height_vec, light_right_pts[1])
        add_vector_to_point(light_right_pts[1], width_vec, light_right_pts[2])
        add_vector_to_point(self.front_right, width_vec, light_right_pts[3])
        
        pygame.draw.polygon(screen, "yellow", light_left_pts)
        pygame.draw.polygon(screen, "yellow", light_right_pts)
    
    def draw_window(self, screen):
        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height / 4, 1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width, 1, self.height)
        window_pts = [[0, 0] for i in range(4)]
        window_pts[0] = self.front_left
        add_vector_to_point(self.front_left, height_vec, window_pts[1])
        add_vector_to_point(self.front_right, height_vec, window_pts[2])
        window_pts[3] = self.front_right
        
        pygame.draw.polygon(screen, "lightblue", window_pts)

    def draw(self, screen):
        pygame.draw.polygon(screen, "orange", self.corners)
        pygame.draw.polygon(screen, "black", self.corners, 3)
        self.draw_lights(screen)

        #self.draw_window(screen)

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