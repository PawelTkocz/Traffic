from enum import Enum
import math

def on_segment(p, q, r):
    #https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
    
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))): 
        return True
    return False
  
def orientation(p, q, r): 
    #https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y)) 
    if (val > 0): 
        return 1
    elif (val < 0): 
        return 2
    else:  
        return 0

def do_intersect(p1, q1, p2, q2): 
    #https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
    o1 = orientation(p1, q1, p2) 
    o2 = orientation(p1, q1, q2) 
    o3 = orientation(p2, q2, p1) 
    o4 = orientation(p2, q2, q1) 
  
    if ((o1 != o2) and (o3 != o4)): 
        return True
  
    if ((o1 == 0) and on_segment(p1, p2, q1)): 
        return True
  
    if ((o2 == 0) and on_segment(p1, q2, q1)): 
        return True
  
    if ((o3 == 0) and on_segment(p2, p1, q2)): 
        return True
  
    if ((o4 == 0) and on_segment(p2, q1, q2)): 
        return True
  
    return False

class TurnDir(Enum):
    RIGHT = 1
    LEFT = 2
    STRAIGHT = 3

class Point: 
    def __init__(self, x, y): 
        self.x = x 
        self.y = y

    def add_vector(self, v, ret_new_point=True):
        if ret_new_point:
            return Point(self.x + v.x, self.y + v.y)
        else:
            self.x += v.x
            self.y += v.y

    def rotate_over_point(self, rotate_point, angle, dir):
        if dir == TurnDir.RIGHT:
            angle = math.pi * 2 - angle
        elif dir != TurnDir.LEFT:
            return
        
        s = math.sin(angle)
        c = math.cos(angle)
        self.x -= rotate_point.x
        self.y -= rotate_point.y
        new_x = self.x * c - self.y * s
        new_y = self.x * s + self.y * c
        self.x = new_x + rotate_point.x
        self.y = new_y + rotate_point.y

    def compare(self, p):
        return self.x == p.x and self.y == p.y

    def copy_coordinates_from(self, p):
        self.x = p.x
        self.y = p.y

class Vector(Point):
    """Vector is represented by single Point - it represents the vector [(0, 0), Point]"""
    
    def __init__(self, b, e):
        super().__init__(e.x - b.x, e.y - b.y)

    def add_vector(self, v, ret_new_vec=True):
        if ret_new_vec:
            return Vector(self.x + v.x, self.y + v.y)
        else:
            self.x += v.x
            self.y += v.y

    def len(self):
        return math.sqrt( self.x **2 + self.y **2) 

    def scale(self, k, ret_new_vec=True):
        if ret_new_vec:
            return Vector(Point(0, 0), Point(self.x * k, self.y * k))
        else:
            self.x *= k
            self.y *= k

    def scale_to_len(self, res_len, ret_new_vec=True):
        if self.len() == 0:
            return self.scale(0, ret_new_vec)
        else:
            k = res_len / self.len()
            return self.scale(k, ret_new_vec)

    def orthogonal_vector(self, vec_len, dir):
        """Creates orthogonal vector that 'turns' right or left depending on dir"""
        
        if dir == TurnDir.RIGHT: 
            orth_vec = Vector(self.y, -1 * self.x)
        elif dir == TurnDir.LEFT:
            orth_vec = Vector(-1 * self.y, self.x)
        else: 
            return Vector(self.x, self.y)

        ort_vec_len = orth_vec.len()
        if ort_vec_len == 0:
            return orth_vec
        else:
            k = vec_len / ort_vec_len
            orth_vec.scale(k, False)
            return orth_vec

    def normalize(self, ret_new_vec=True):
        new_vec = self.scale_to_len(1)
        if ret_new_vec:
            return new_vec
        else:
            self.x = new_vec.x
            self.y = new_vec.y
    
    def copy(self):
        return Vector((0, 0), Point(self.x, self.y))

class Rectangle():
    """Class representing 'directed' rectangle - with front, left and right side, and rear"""
    def __init__(self, front_left, width, length, direction):
        self.width = width
        self.length = self.length
        self.front_left = Point(front_left.x, front_left.y)
        width_vec = direction.orthogonal_vector(width, TurnDir.RIGHT)
        length_vec = width_vec.orthogonal_vector(length, TurnDir.RIGHT)
        self.front_right = self.front_left.add_vector(width_vec)
        self.rear_left = self.front_left.add_vector(length_vec)
        self.rear_right = self.rear_left.add_vector(width_vec)

    def find_cur_direction(self):
        return Vector(self.rear_right, self.front_right).normalize(False)

    def move_left_side(self, front_vec, rear_vec):
        self.front_left.add_vector(front_vec, False)
        self.rear_left.add_vector(rear_vec, False)
        v = Vector(self.rear_left, self.front_left).scale_to_len(self.length, False)
        self.front_left = self.rear_left.add_vector(v)
        self.find_right_side()
        return self.find_cur_direction()

    def move_right_side(self, front_vec, rear_vec):
        self.front_right.add_vector(front_vec, False)
        self.rear_right.add_vector(rear_vec, False)
        v = Vector(self.rear_right, self.front_right).scale_to_len(self.length, False)
        self.front_right = self.rear_right.add_vector(v)
        self.find_left_side()
        return self.find_cur_direction()

    def find_left_side(self):
        width_vec = Vector(self.rear_right, self.front_right).orthogonal_vector(self.width, TurnDir.LEFT)
        self.front_left = self.front_right.add_vector(width_vec)
        self.rear_left = self.rear_right.add_vector(width_vec)

    def find_right_corners(self):
        width_vec = Vector(self.rear_left, self.front_left).orthogonal_vector(self.width, TurnDir.RIGHT)
        self.front_right = self.front_left.add_vector(width_vec)
        self.rear_right = self.rear_left.add_vector(width_vec)

    def collides(self, rec):
        self_corners = [self.rear_left, self.rear_right, self.front_right, self.front_left]
        rec_corners = [rec.rear_left, rec.rear_right, rec.front_right, rec.front_left]
        self_sides = [(self_corners[i], self_corners[(i+1) % 4]) for i in range(4)]
        rec_sides = [(rec_corners[i], rec_corners[(i+1) % 4]) for i in range(4)]
        return any([do_intersect(s1[0], s1[1], s2[0], s2[1]) for s1 in self_sides for s2 in rec_sides])