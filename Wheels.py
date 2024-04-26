import math

def move_point(p, vec, vec_len):
    p[0] += vec[0]*vec_len
    p[1] += vec[1]*vec_len
    return p

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

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

class Wheels:
    def __init__(self, max_angle):
        self.max_angle = max_angle
        self.max_left_direction = rotate_over_point([0, 1], (0, 0), max_angle, -1)
        self.max_right_direction = rotate_over_point([0, 1], (0, 0), max_angle, 1)
        self.direction = [0, 1]

    def cur_wheel_angle(self, car):
        x1 = self.direction[0]
        y1 = self.direction[1]
        x2 = car.front_left[0] - car.rear_left[0]
        y2 = car.front_left[1] - car.rear_left[1]
        dot = x1*x2 + y1*y2
        det = x1*y2 - y1*x2
        return math.atan2(det, dot)

    def turn(self, angle, dir):
        self.direction = rotate_over_point(self.direction, (0, 0), angle, dir)
        if self.direction[0] < self.max_left_direction[0]:
            self.direction = self.max_left_direction
        elif self.direction[1] > self.max_right_direction[1]:
            self.direction = self.max_right_direction

    def move_front_wheels(self, corners, vel):
        rear_left, rear_right, front_right, front_left = corners
        if self.direction[0] > -1:
            #turn right
            move_point(front_right, self.direction, vel)
            rotate_point_vec = [rear_right[0] - rear_left[0], rear_right[1] - rear_left[1]]
            if self.direction[0] == 0:
                vec_len = 1000000
            else: vec_len = math.pi / 2 / self.direction[0]
            #vec_len = self.direction / (math.pi / 2)
            rotate_point = [rear_left[0] + rotate_point_vec[0]*vec_len, rear_left[1] + rotate_point_vec[1]*vec_len]
            rotate_over_point(front_left, rotate_point, vel/distance(rotate_point, front_left), 1)