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
        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height // 15, 1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 4, 1, self.height)   
        light_left_pts[0] = self.front_left[:]
        add_vector_to_point(self.front_left, height_vec, light_left_pts[1])
        add_vector_to_point(light_left_pts[1], width_vec, light_left_pts[2])
        add_vector_to_point(self.front_left, width_vec, light_left_pts[3])

        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 4, -1, self.height)   
        light_right_pts[0] = self.front_right[:]
        add_vector_to_point(self.front_right, height_vec, light_right_pts[1])
        add_vector_to_point(light_right_pts[1], width_vec, light_right_pts[2])
        add_vector_to_point(self.front_right, width_vec, light_right_pts[3])

        pygame.draw.polygon(screen, "yellow", light_left_pts)
        pygame.draw.polygon(screen, "yellow", light_right_pts)
    
    def draw_wing_mirrors(self, screen):
        mirror_left_pts = [[0, 0] for i in range(4)]
        mirror_right_pts = [[0, 0] for i in range(4)]

        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height // 4, 1, self.width)      
        add_vector_to_point(self.front_left, height_vec, mirror_left_pts[0])
        add_vector_to_point(self.front_right, height_vec, mirror_right_pts[0])

        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height // 20, 1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 8, -1, self.height)   

        add_vector_to_point(mirror_left_pts[0], height_vec, mirror_left_pts[1])
        add_vector_to_point(mirror_left_pts[1], width_vec, mirror_left_pts[2])
        add_vector_to_point(mirror_left_pts[0], width_vec, mirror_left_pts[3])

        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 8, 1, self.height) 
        add_vector_to_point(mirror_right_pts[0], height_vec, mirror_right_pts[1])
        add_vector_to_point(mirror_right_pts[1], width_vec, mirror_right_pts[2])
        add_vector_to_point(mirror_right_pts[0], width_vec, mirror_right_pts[3])

        pygame.draw.polygon(screen, "black", mirror_left_pts)
        pygame.draw.polygon(screen, "black", mirror_right_pts)        

    def draw_front_window(self, screen):
        pts = [[0, 0] for i in range(4)]
         
        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height * 4 // 15, 1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 8, 1, self.height)         
        add_vector_to_point(self.front_left, height_vec, pts[0])
        add_vector_to_point(pts[0], width_vec, pts[0])
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width * 0.75, 1, self.height) 
        add_vector_to_point(pts[0], width_vec, pts[1])

        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height // 7, 1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 8, 1, self.height) 
        add_vector_to_point(pts[0], width_vec, pts[3])
        add_vector_to_point(pts[3], height_vec, pts[3])
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 2, 1, self.height)
        add_vector_to_point(pts[3], width_vec, pts[2])
        pygame.draw.polygon(screen, "black", pts)

    def draw_side_windows(self, screen):
        pts_left = [[0, 0] for i in range(4)]
        pts_right = [[0, 0] for i in range(4)]

        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height * 0.4, 1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 8, 1, self.height)         
        add_vector_to_point(self.front_left, height_vec, pts_left[0])
        add_vector_to_point(pts_left[0], width_vec, pts_left[0])

        add_vector_to_point(self.front_right, height_vec, pts_right[0])
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 8, -1, self.height)
        add_vector_to_point(pts_right[0], width_vec, pts_right[0])

        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 8, 1, self.height) 
        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height / 15, 1, self.width)
        add_vector_to_point(pts_left[0], width_vec, pts_left[1])
        add_vector_to_point(pts_left[1], height_vec, pts_left[1])
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 8, -1, self.height) 
        add_vector_to_point(pts_right[0], width_vec, pts_right[1])
        add_vector_to_point(pts_right[1], height_vec, pts_right[1])        

        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height * 4 / 15, 1, self.width)
        add_vector_to_point(pts_left[1], height_vec, pts_left[2])
        add_vector_to_point(pts_right[1], height_vec, pts_right[2])

        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height * 6 / 15, 1, self.width)
        add_vector_to_point(pts_left[0], height_vec, pts_left[3])
        add_vector_to_point(pts_right[0], height_vec, pts_right[3])
        pygame.draw.polygon(screen, "black", pts_left)
        pygame.draw.polygon(screen, "black", pts_right)

    def draw_back_window(self, screen):
        pts = [[0, 0] for i in range(4)]
         
        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height // 7, -1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 4, 1, self.height)         
        add_vector_to_point(self.rear_left, height_vec, pts[0])
        add_vector_to_point(pts[0], width_vec, pts[0])
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 2, 1, self.height) 
        add_vector_to_point(pts[0], width_vec, pts[1])

        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height // 15, -1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 8, 1, self.height) 
        add_vector_to_point(pts[0], width_vec, pts[3])
        add_vector_to_point(pts[3], height_vec, pts[3])
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 4, 1, self.height)
        add_vector_to_point(pts[3], width_vec, pts[2])
        pygame.draw.polygon(screen, "black", pts)

    def draw_wheels(self, screen):
        wheel_left_pts = [[0, 0] for i in range(4)]
        wheel_right_pts = [[0, 0] for i in range(4)]

        wheel_left_pts[0] = self.front_left[:]
        wheel_right_pts[0] = self.front_right[:]
        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height // 4, 1, self.width)      
        add_vector_to_point(self.front_left, height_vec, wheel_left_pts[1])
        add_vector_to_point(self.front_right, height_vec, wheel_right_pts[1]) 
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 8, 1, self.height)   
        add_vector_to_point(wheel_left_pts[0], width_vec, wheel_left_pts[3])
        add_vector_to_point(wheel_left_pts[1], width_vec, wheel_left_pts[2])
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 8, -1, self.height)   
        add_vector_to_point(wheel_right_pts[0], width_vec, wheel_right_pts[3])
        add_vector_to_point(wheel_right_pts[1], width_vec, wheel_right_pts[2])

        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 16, 1, self.height)   
        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height // 8, 1, self.width)  
        rotate_point_left = [0, 0]
        add_vector_to_point(self.front_left, height_vec, rotate_point_left)
        add_vector_to_point(rotate_point_left, width_vec, rotate_point_left)
        rotate_point_right = [0, 0]
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 16, -1, self.height)   
        add_vector_to_point(self.front_right, height_vec, rotate_point_right)
        add_vector_to_point(rotate_point_right, width_vec, rotate_point_right)
        rotate_dir = -1
        if self.wheels.is_turn_right():
            rotate_dir = 1

        wheel_left_pts = [Wheels.rotate_over_point(p, rotate_point_left, self.wheels.cur_wheel_angle(), rotate_dir) for p in wheel_left_pts]
        wheel_right_pts = [Wheels.rotate_over_point(p, rotate_point_right, self.wheels.cur_wheel_angle(), rotate_dir) for p in wheel_right_pts]

        pygame.draw.polygon(screen, "#262626", wheel_left_pts)
        pygame.draw.polygon(screen, "#262626", wheel_right_pts)   

    def draw_inside(self, screen):
        #1/20 of width
        pts = [[0, 0] for i in range(4)]
        line_width = self.width // 20  
        height_vec = orthogonal_vector(self.front_left, self.front_right, line_width, -1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, line_width, 1, self.height)         
        add_vector_to_point(self.rear_left, height_vec, pts[0])
        add_vector_to_point(pts[0], width_vec, pts[0])

        height_vec = orthogonal_vector(self.front_left, self.front_right, self.height * 14 / 15 - line_width, -1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width * 0.9, 1, self.height) 

        add_vector_to_point(pts[0], height_vec, pts[1])
        add_vector_to_point(pts[1], width_vec, pts[2])
        add_vector_to_point(pts[0], width_vec, pts[3])
        pygame.draw.polygon(screen, "orange", pts)

    def draw(self, screen):
        self.draw_wheels(screen)
        pygame.draw.polygon(screen, "black", self.corners)
        self.draw_inside(screen)
        self.draw_lights(screen)
        self.draw_wing_mirrors(screen)
        self.draw_front_window(screen)
        self.draw_side_windows(screen)
        self.draw_back_window(screen)

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