import pygame
import Wheels
from Wheels import rotate_over_point

class CarDrafter:
    """Class responsible for drawing car on the screen"""
    def __init__(self, width, length, color):
        self.width = width
        self.length = length
        self.color = color

    def draw_lights(self):
        light_left_pts = [[0, 0] for i in range(4)]
        light_right_pts = [[0, 0] for i in range(4)]
        length_vec = orthogonal_vector(self.front_left, self.front_right, self.length // 15, 1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 4, 1, self.length)   
        light_left_pts[0] = self.front_left[:]
        add_vector_to_point(self.front_left, length_vec, light_left_pts[1])
        add_vector_to_point(light_left_pts[1], width_vec, light_left_pts[2])
        add_vector_to_point(self.front_left, width_vec, light_left_pts[3])

        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 4, -1, self.length)   
        light_right_pts[0] = self.front_right[:]
        add_vector_to_point(self.front_right, length_vec, light_right_pts[1])
        add_vector_to_point(light_right_pts[1], width_vec, light_right_pts[2])
        add_vector_to_point(self.front_right, width_vec, light_right_pts[3])

        pygame.draw.polygon(self.screen, "yellow", light_left_pts)
        pygame.draw.polygon(self.screen, "yellow", light_right_pts)
    
    def draw_wing_mirrors(self):
        mirror_left_pts = [[0, 0] for i in range(4)]
        mirror_right_pts = [[0, 0] for i in range(4)]

        length_vec = orthogonal_vector(self.front_left, self.front_right, self.length // 4, 1, self.width)      
        add_vector_to_point(self.front_left, length_vec, mirror_left_pts[0])
        add_vector_to_point(self.front_right, length_vec, mirror_right_pts[0])

        length_vec = orthogonal_vector(self.front_left, self.front_right, self.length // 20, 1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 8, -1, self.length)   

        add_vector_to_point(mirror_left_pts[0], length_vec, mirror_left_pts[1])
        add_vector_to_point(mirror_left_pts[1], width_vec, mirror_left_pts[2])
        add_vector_to_point(mirror_left_pts[0], width_vec, mirror_left_pts[3])

        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 8, 1, self.length) 
        add_vector_to_point(mirror_right_pts[0], length_vec, mirror_right_pts[1])
        add_vector_to_point(mirror_right_pts[1], width_vec, mirror_right_pts[2])
        add_vector_to_point(mirror_right_pts[0], width_vec, mirror_right_pts[3])

        pygame.draw.polygon(self.screen, "black", mirror_left_pts)
        pygame.draw.polygon(self.screen, "black", mirror_right_pts)        

    def draw_front_window(self):
        pts = [[0, 0] for i in range(4)]
         
        length_vec = orthogonal_vector(self.front_left, self.front_right, self.length * 4 // 15, 1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 8, 1, self.length)         
        add_vector_to_point(self.front_left, length_vec, pts[0])
        add_vector_to_point(pts[0], width_vec, pts[0])
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width * 0.75, 1, self.length) 
        add_vector_to_point(pts[0], width_vec, pts[1])

        length_vec = orthogonal_vector(self.front_left, self.front_right, self.length // 7, 1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 8, 1, self.length) 
        add_vector_to_point(pts[0], width_vec, pts[3])
        add_vector_to_point(pts[3], length_vec, pts[3])
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 2, 1, self.length)
        add_vector_to_point(pts[3], width_vec, pts[2])
        pygame.draw.polygon(self.screen, "black", pts)

    def draw_side_windows(self):
        pts_left = [[0, 0] for i in range(4)]
        pts_right = [[0, 0] for i in range(4)]

        length_vec = orthogonal_vector(self.front_left, self.front_right, self.length * 0.4, 1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 8, 1, self.length)         
        add_vector_to_point(self.front_left, length_vec, pts_left[0])
        add_vector_to_point(pts_left[0], width_vec, pts_left[0])

        add_vector_to_point(self.front_right, length_vec, pts_right[0])
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 8, -1, self.length)
        add_vector_to_point(pts_right[0], width_vec, pts_right[0])

        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 8, 1, self.length) 
        length_vec = orthogonal_vector(self.front_left, self.front_right, self.length / 15, 1, self.width)
        add_vector_to_point(pts_left[0], width_vec, pts_left[1])
        add_vector_to_point(pts_left[1], length_vec, pts_left[1])
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 8, -1, self.length) 
        add_vector_to_point(pts_right[0], width_vec, pts_right[1])
        add_vector_to_point(pts_right[1], length_vec, pts_right[1])        

        length_vec = orthogonal_vector(self.front_left, self.front_right, self.length * 4 / 15, 1, self.width)
        add_vector_to_point(pts_left[1], length_vec, pts_left[2])
        add_vector_to_point(pts_right[1], length_vec, pts_right[2])

        length_vec = orthogonal_vector(self.front_left, self.front_right, self.length * 6 / 15, 1, self.width)
        add_vector_to_point(pts_left[0], length_vec, pts_left[3])
        add_vector_to_point(pts_right[0], length_vec, pts_right[3])
        pygame.draw.polygon(self.screen, "black", pts_left)
        pygame.draw.polygon(self.screen, "black", pts_right)

    def draw_back_window(self):
        pts = [[0, 0] for i in range(4)]
         
        length_vec = orthogonal_vector(self.front_left, self.front_right, self.length // 7, -1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 4, 1, self.length)         
        add_vector_to_point(self.rear_left, length_vec, pts[0])
        add_vector_to_point(pts[0], width_vec, pts[0])
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 2, 1, self.length) 
        add_vector_to_point(pts[0], width_vec, pts[1])

        length_vec = orthogonal_vector(self.front_left, self.front_right, self.length // 15, -1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width / 8, 1, self.length) 
        add_vector_to_point(pts[0], width_vec, pts[3])
        add_vector_to_point(pts[3], length_vec, pts[3])
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 4, 1, self.length)
        add_vector_to_point(pts[3], width_vec, pts[2])
        pygame.draw.polygon(self.screen, "black", pts)

    def draw_wheels(self):
        wheel_left_pts = [[0, 0] for i in range(4)]
        wheel_right_pts = [[0, 0] for i in range(4)]

        wheel_left_pts[0] = self.front_left[:]
        wheel_right_pts[0] = self.front_right[:]
        length_vec = orthogonal_vector(self.front_left, self.front_right, self.length // 4, 1, self.width)      
        add_vector_to_point(self.front_left, length_vec, wheel_left_pts[1])
        add_vector_to_point(self.front_right, length_vec, wheel_right_pts[1]) 
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 8, 1, self.length)   
        add_vector_to_point(wheel_left_pts[0], width_vec, wheel_left_pts[3])
        add_vector_to_point(wheel_left_pts[1], width_vec, wheel_left_pts[2])
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 8, -1, self.length)   
        add_vector_to_point(wheel_right_pts[0], width_vec, wheel_right_pts[3])
        add_vector_to_point(wheel_right_pts[1], width_vec, wheel_right_pts[2])

        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 16, 1, self.length)   
        length_vec = orthogonal_vector(self.front_left, self.front_right, self.length // 8, 1, self.width)  
        rotate_point_left = [0, 0]
        add_vector_to_point(self.front_left, length_vec, rotate_point_left)
        add_vector_to_point(rotate_point_left, width_vec, rotate_point_left)
        rotate_point_right = [0, 0]
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width // 16, -1, self.length)   
        add_vector_to_point(self.front_right, length_vec, rotate_point_right)
        add_vector_to_point(rotate_point_right, width_vec, rotate_point_right)
        rotate_dir = -1
        if self.is_turn_right:
            rotate_dir = 1

        wheel_left_pts = [rotate_over_point(p, rotate_point_left, self.wheels_angle, rotate_dir) for p in wheel_left_pts]
        wheel_right_pts = [rotate_over_point(p, rotate_point_right, self.wheels_angle, rotate_dir) for p in wheel_right_pts]

        pygame.draw.polygon(self.screen, "#262626", wheel_left_pts)
        pygame.draw.polygon(self.screen, "#262626", wheel_right_pts)   

    def draw_inside(self):
        pts = [[0, 0] for i in range(4)]
        line_width = self.width // 20  
        length_vec = orthogonal_vector(self.front_left, self.front_right, line_width, -1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, line_width, 1, self.length)         
        add_vector_to_point(self.rear_left, length_vec, pts[0])
        add_vector_to_point(pts[0], width_vec, pts[0])

        length_vec = orthogonal_vector(self.front_left, self.front_right, self.length * 14 / 15 - line_width, -1, self.width)
        width_vec = orthogonal_vector(self.rear_left, self.front_left, self.width * 0.9, 1, self.length) 

        add_vector_to_point(pts[0], length_vec, pts[1])
        add_vector_to_point(pts[1], width_vec, pts[2])
        add_vector_to_point(pts[0], width_vec, pts[3])
        pygame.draw.polygon(self.screen, self.color, pts)

    def draw(self, corners, wheels_angle, is_turn_right, screen):
        self.wheels_angle = wheels_angle
        self.is_turn_right = is_turn_right
        self.rear_left, self.rear_right, self.front_right, self.front_left = corners
        self.screen = screen

        self.draw_wheels()
        pygame.draw.polygon(screen, "black", corners)
        self.draw_inside()
        self.draw_lights()
        self.draw_wing_mirrors()
        self.draw_front_window()
        self.draw_side_windows()
        self.draw_back_window()