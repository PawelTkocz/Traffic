import math

def rotate_over_point(p, rotate_point, angle, dir):
    if dir == 1:
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

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

class Wheels:
    def __init__(self, max_angle):
        self.max_angle = max_angle
        self.max_left_direction = rotate_over_point([1, 0], (0, 0), max_angle, -1)
        self.max_right_direction = rotate_over_point([1, 0], (0, 0), max_angle, 1)
        self.direction = [1, 0]

    def is_turn_right(self):
        return self.direction[1] < 0

    def sin_cur_angle(self):
        return abs(self.direction[1])
    
    def cos_cur_angle(self):
        return self.direction[0]

    def cur_wheel_angle(self):
        #kat odchylenia od osi wyprostowanych kół
        return math.acos(self.direction[0])

    def cur_movement_direction(self, car_dir):
        mov_dir = car_dir[:]

        if self.is_turn_right(): rotate_dir = 1 
        else: rotate_dir = -1

        rotate_over_point(mov_dir, (0, 0), self.cur_wheel_angle(), rotate_dir)
        return mov_dir
        
    def turn(self, angle, dir):
        #change wheels position
        self.direction = rotate_over_point(self.direction, (0, 0), angle, dir)
        if self.direction[1] > self.max_left_direction[1]:
            self.direction[:] = self.max_left_direction
        elif self.direction[1] < self.max_right_direction[1]:
            self.direction[:] = self.max_right_direction
