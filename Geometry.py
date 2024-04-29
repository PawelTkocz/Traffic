#pytanie czy w wektorze chcemy robi kopie

from enum import Enum
import math

class TurnDir(Enum):
    RIGHT = 1
    LEFT = 2

def distance(p1, p2):
        return math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2) 

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
            return Vector(self.x * k, self.y * k)
        else:
            self.x *= k
            self.y *= k

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

class Rectangle():
    """Class representing 'directed' rectangle - with front, left and right side, and rear"""
    def __init__(self, front_left, direction):
        #direction should be represented as vector [x, y]
        self.front_left = front_left