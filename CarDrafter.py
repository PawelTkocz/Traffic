import pygame

from Geometry import Point, TurnDir, Vector

class CarDrafter:
    """Class responsible for drawing car on the screen"""
    def __init__(self, width, length, color):
        self.width = width
        self.length = length
        self.color = color

    def draw_lights(self):
        light_left_pts = [Point(0, 0) for i in range(4)]
        light_right_pts = [Point(0, 0) for i in range(4)]
        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(self.length // 15, TurnDir.RIGHT)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width // 4, TurnDir.RIGHT) 
        light_left_pts[0].copy_coordinates_from(self.front_left)
        light_left_pts[1] = self.front_left.add_vector(length_vec)
        light_left_pts[2] = light_left_pts[1].add_vector(width_vec)
        light_left_pts[3] = self.front_left.add_vector(width_vec)

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width // 4, TurnDir.LEFT)   
        light_right_pts[0].copy_coordinates_from(self.front_right)
        light_right_pts[1] = self.front_right.add_vector(length_vec)
        light_right_pts[2] = light_right_pts[1].add_vector(width_vec)
        light_right_pts[3] = self.front_right.add_vector(width_vec)

        pygame.draw.polygon(self.screen, "yellow", [(p.x, p.y) for p in light_left_pts])
        pygame.draw.polygon(self.screen, "yellow", [(p.x, p.y) for p in light_right_pts])
    
    def draw_wing_mirrors(self):
        mirror_left_pts = [Point(0, 0) for i in range(4)]
        mirror_right_pts = [Point(0, 0) for i in range(4)]

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(self.length // 4, TurnDir.RIGHT)
        mirror_left_pts[0] = self.front_left.add_vector(length_vec)
        mirror_right_pts[0] = self.front_right.add_vector(length_vec)

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(self.length // 20, TurnDir.RIGHT)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width // 8, TurnDir.LEFT)

        mirror_left_pts[1] = mirror_left_pts[0].add_vector(length_vec)
        mirror_left_pts[2] = mirror_left_pts[1].add_vector(width_vec)
        mirror_left_pts[3] = mirror_left_pts[0].add_vector(width_vec)

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width // 8, TurnDir.RIGHT)
        mirror_right_pts[1] = mirror_right_pts[0].add_vector(length_vec)
        mirror_right_pts[2] = mirror_right_pts[1].add_vector(width_vec)
        mirror_right_pts[3] = mirror_right_pts[0].add_vector(width_vec)

        pygame.draw.polygon(self.screen, "black", [(p.x, p.y) for p in mirror_left_pts])
        pygame.draw.polygon(self.screen, "black", [(p.x, p.y) for p in mirror_right_pts])        

    def draw_front_window(self):
        pts = [Point(0, 0) for i in range(4)]
        
        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(self.length * 4 // 15, TurnDir.RIGHT)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width / 8, TurnDir.RIGHT)

        pts[0] = self.front_left.add_vector(length_vec).add_vector(width_vec)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width * 0.75, TurnDir.RIGHT)
        pts[1] = pts[0].add_vector(width_vec)

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(self.length // 7, TurnDir.RIGHT)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width / 8, TurnDir.RIGHT)
        pts[3] = pts[0].add_vector(width_vec).add_vector(length_vec)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width // 2, TurnDir.RIGHT)
        pts[2] = pts[3].add_vector(width_vec)

        pygame.draw.polygon(self.screen, "black", [(p.x, p.y) for p in pts])

    def draw_side_windows(self):
        pts_left = [Point(0, 0) for i in range(4)]
        pts_right = [Point(0, 0) for i in range(4)]

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(self.length * 0.4, TurnDir.RIGHT)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width / 8, TurnDir.RIGHT)
        pts_left[0] = self.front_left.add_vector(length_vec).add_vector(width_vec)

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width / 8, TurnDir.LEFT)
        pts_right[0] = self.front_right.add_vector(length_vec).add_vector(width_vec)

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(self.length / 15, TurnDir.RIGHT)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width / 8, TurnDir.RIGHT)
        pts_left[1] = pts_left[0].add_vector(width_vec).add_vector(length_vec)

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width / 8, TurnDir.LEFT)
        pts_right[1] = pts_right[0].add_vector(width_vec).add_vector(length_vec)
             
        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(self.length * 4 / 15, TurnDir.RIGHT)
        pts_left[2] = pts_left[1].add_vector(length_vec)
        pts_right[2] = pts_right[1].add_vector(length_vec)

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(self.length * 6 / 15, TurnDir.RIGHT)
        pts_left[3] = pts_left[0].add_vector(length_vec)
        pts_right[3] = pts_right[0].add_vector(length_vec)        

        pygame.draw.polygon(self.screen, "black", [(p.x, p.y) for p in pts_left])
        pygame.draw.polygon(self.screen, "black", [(p.x, p.y) for p in pts_right])

    def draw_back_window(self):
        pts = [Point(0, 0) for i in range(4)]
         
        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(self.length // 7, TurnDir.LEFT)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width / 4, TurnDir.RIGHT)
        pts[0] = self.rear_left.add_vector(length_vec).add_vector(width_vec)

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width / 2, TurnDir.RIGHT)
        pts[1] = pts[0].add_vector(width_vec)

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(self.length // 15, TurnDir.LEFT)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width / 8, TurnDir.RIGHT)
        pts[3] = pts[0].add_vector(width_vec).add_vector(length_vec)    

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width // 4, TurnDir.RIGHT)
        pts[2] = pts[3].add_vector(width_vec)

        pygame.draw.polygon(self.screen, "black", [(p.x, p.y) for p in pts])

    def draw_wheels(self):
        wheel_left_pts = [Point(0, 0) for i in range(4)]
        wheel_right_pts = [Point(0, 0) for i in range(4)]

        wheel_left_pts[0].copy_coordinates_from(self.front_left)
        wheel_right_pts[0].copy_coordinates_from(self.front_right)
        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(self.length // 4, TurnDir.RIGHT)
        wheel_left_pts[1] = self.front_left.add_vector(length_vec)    
        wheel_right_pts[1] = self.front_right.add_vector(length_vec)    
        
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width //8, TurnDir.RIGHT)
        wheel_left_pts[3] = wheel_left_pts[0].add_vector(width_vec) 
        wheel_left_pts[2] = wheel_left_pts[1].add_vector(width_vec) 

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width //8, TurnDir.LEFT)
        wheel_right_pts[3] = wheel_right_pts[0].add_vector(width_vec) 
        wheel_right_pts[2] = wheel_right_pts[1].add_vector(width_vec) 

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(self.length // 8, TurnDir.RIGHT)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width / 16, TurnDir.RIGHT)  
        rotate_point_left = self.front_left.add_vector(length_vec).add_vector(width_vec)

        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width // 16, TurnDir.LEFT) 
        rotate_point_right = self.front_right.add_vector(length_vec).add_vector(width_vec) 

        for p1, p2 in zip(wheel_left_pts, wheel_right_pts):
            p1.rotate_over_point(rotate_point_left, self.wheels_angle, self.cur_turn_side)
            p2.rotate_over_point(rotate_point_right, self.wheels_angle, self.cur_turn_side)

        pygame.draw.polygon(self.screen, "#262626", [(p.x, p.y) for p in wheel_left_pts])
        pygame.draw.polygon(self.screen, "#262626", [(p.x, p.y) for p in wheel_right_pts])   

    def draw_inside(self):
        pts = [Point(0, 0) for i in range(4)]
        line_width = self.width // 20  

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(line_width, TurnDir.LEFT)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(line_width, TurnDir.RIGHT)  
        pts[0] = self.rear_left.add_vector(length_vec).add_vector(width_vec)

        length_vec = Vector(self.front_left, self.front_right).orthogonal_vector(self.length * 14 / 15 - line_width, TurnDir.LEFT)
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width * 0.9, TurnDir.RIGHT) 

        pts[1] = pts[0].add_vector(length_vec)
        pts[2] = pts[1].add_vector(width_vec)
        pts[3] = pts[0].add_vector(width_vec)

        pygame.draw.polygon(self.screen, self.color, [(p.x, p.y) for p in pts])

    def draw(self, corners, wheels_angle, cur_turn_side, screen):
        self.wheels_angle = wheels_angle
        self.cur_turn_side = cur_turn_side
        self.rear_left, self.rear_right, self.front_right, self.front_left = corners
        self.screen = screen

        self.draw_wheels()
        pygame.draw.polygon(screen, "black", [(p.x, p.y) for p in corners])
        self.draw_inside()
        self.draw_lights()
        self.draw_wing_mirrors()
        self.draw_front_window()
        self.draw_side_windows()
        self.draw_back_window()