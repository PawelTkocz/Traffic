import CarDrafter
from Wheels import Wheels
from Geometry import TurnDir, Vector, Point, Rectangle
import math

class Car:
    """Class simulating functioning of car in Cartesian coordinate system"""
    turning_speed = 0.05
    acceleration = 0.1
    max_speed = 10
    brake_val = 0.1
    resistance = 0.03

    def __init__(self, width, length, front_left_pos, direction, wheels_max_turn, *, color):
        self.width = width
        self.length = length
        if direction.x == 0 and direction.y == 0:
            self.direction = Vector(Point(0, 0), Point(1, 0))
        else:
            self.direction = Vector(Point(0, 0), Point(direction.x, direction.y)).normalize(True)

        self.corners = Rectangle(front_left_pos, width, length, self.direction)
        self.wheels = Wheels(wheels_max_turn)
        self.vel = 0
        self.car_drafter = CarDrafter.CarDrafter(width, length, color)

    def speed_up_front(self, limit=None):
        if self.vel >= 0:
            if limit is None or limit > self.max_speed:
                self.vel += self.acceleration
                self.vel = min(self.vel, self.max_speed)
            elif self.vel <= limit:
                self.vel += self.acceleration
                self.vel = min(self.vel, limit)
            else:
                self.brake()
                self.vel = max(self.vel, limit)

    def speed_up_reverse(self, limit=None):
        if self.vel <= 0:
            if limit is None or limit < -1 * self.max_speed:
                self.vel -= self.acceleration
                self.vel = max(self.vel, -1 * self.max_speed)
            elif self.vel >= limit:
                self.vel -= self.acceleration
                self.vel = max(self.vel, limit)
            else:
                self.brake()
                self.vel = min(self.vel, limit)

    def slow_down(self, vel):
        if self.vel > 0:
            self.vel -= vel
            self.vel = max(0, self.vel)
        elif self.vel < 0:
            self.vel += vel
            self.vel = min(0, self.vel)

    def brake(self):
        self.slow_down(self.brake_val)

    def turn_left(self):
        self.wheels.turn(self.turning_speed, TurnDir.LEFT)

    def turn_right(self):
        self.wheels.turn(self.turning_speed, TurnDir.RIGHT)

    def which_side_turn(self):
        return self.wheels.which_side_turn()

    def straighten_wheels(self):
        turn_side = self.which_side_turn()
        if turn_side == TurnDir.RIGHT:
            self.turn_left()
            if self.which_side_turn() != TurnDir.RIGHT:
                self.wheels.make_straight()
        elif turn_side == TurnDir.LEFT:
            self.turn_right()
            if self.which_side_turn() != TurnDir.LEFT:
                self.wheels.make_straight()

    def draw(self, screen):
        crnrs = self.corners.get_corners_list()
        self.car_drafter.draw(crnrs, self.wheels.cur_wheel_angle(), self.which_side_turn(), screen)

    def cur_movement_vector(self):
        mov_dir = self.direction.copy()
        mov_dir.rotate_over_point(Point(0, 0), self.wheels.cur_wheel_angle(), self.which_side_turn())
        mov_dir.scale_to_len(self.vel, False)
        return mov_dir

    def move(self):
        if self.vel == 0:
            return
        front_movement_vec = self.cur_movement_vector()
        rear_vel =  (self.length
                     - math.sqrt(self.length**2 - self.vel**2 * self.wheels.sin_cur_angle()**2)
                     + self.vel * self.wheels.cos_cur_angle())
        rear_movement_vec = self.direction.scale_to_len(rear_vel, True)
        if self.which_side_turn() == TurnDir.RIGHT:
            self.direction = self.corners.move_right_side(front_movement_vec, rear_movement_vec)
        else:
            self.direction = self.corners.move_left_side(front_movement_vec, rear_movement_vec)

        self.slow_down(self.resistance)

    def collides_car(self, car):
        return self.corners.collides(car.corners)