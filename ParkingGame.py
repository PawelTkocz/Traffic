import pygame
import CarFactory
import BackgroundDrafter
import math
from sys import exit

from CarDrafter import tuples_list
from Geometry import Point, Vector

class ParkingGame:
    screen_height = 800
    screen_width = 1400
    def __init__(self):
        self.car_factory = CarFactory.CarFactory()
        self.car_length = 360
        self.car_width = 200
        offset_x = (self.screen_width - 3.5 * self.car_length) // 2
        offset_y = self.screen_height - 1.5 * self.car_width
        self.wheel_max_angle = math.pi / 3

        self.c1 = self.car_factory.get_car(self.car_width, self.car_length, 
                                            Point(offset_x + self.car_length, offset_y),
                                            Vector(1, 0), self.wheel_max_angle, color="#4287f5")
        self.c2 = self.car_factory.get_car(self.car_width, self.car_length, 
                                            Point(offset_x + 3.5 * self.car_length, offset_y), 
                                            Vector(1, 0), self.wheel_max_angle, color="#e8e531")
        self.c3 = self.car_factory.get_car(self.car_width, self.car_length, 
                                            Point(1.5 * self.car_length, 243),
                                            Vector(1, 0), self.wheel_max_angle, color="#b82f11")

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen_rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)
        self.background_drafter = BackgroundDrafter.BackgroundDrafter(self.screen_width, self.screen_height)
        self.parking_spot_color = "#e60000"

        margin = 10
        self.parking_spot = pygame.Rect(offset_x + self.car_length + margin, offset_y - margin,
                                         1.5 * self.car_length - 2 * margin, self.car_width + 2*margin)

    def draw(self):
        self.background_drafter.draw(self.screen)
        pygame.draw.rect(self.screen, self.parking_spot_color, self.parking_spot, 15)
        self.c1.draw(self.screen)
        self.c2.draw(self.screen)
        self.c3.draw(self.screen)

    def restart(self):
        self.c3 = self.car_factory.get_car(self.car_width, self.car_length, 
                                            Point(1.5 * self.car_length, 243),
                                            Vector(1, 0), self.wheel_max_angle, color="#b82f11")
        self.parking_spot_color = "#e60000"

    def turn_left(self):
        self.c3.turn_left()

    def turn_right(self):
        self.c3.turn_right()

    def speed_up_front(self):
        self.c3.speed_up_front()

    def brake(self):
        self.c3.brake()

    def speed_up_reverse(self):
        self.c3.speed_up_reverse()

    def parking_succeeded(self):
        return all([self.parking_spot.collidepoint(c) for c in tuples_list(self.c3.get_corners_list())])

    def game_over(self):
        if not all([self.screen_rect.collidepoint(c) for c in tuples_list(self.c3.get_corners_list())]):
            return True
        if self.c3.collides_car(self.c1) or self.c3.collides_car(self.c2):
            return True
        return False

    def next_frame(self):
        self.c3.move()

        if self.parking_succeeded():
            self.parking_spot_color = "#00e600"
        else:
            self.parking_spot_color = "#e60000"
        
        if self.game_over():
            self.restart()

pygame.init()
clock = pygame.time.Clock()
game = ParkingGame()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        game.turn_left()
    elif keys[pygame.K_RIGHT]:
        game.turn_right()
    if keys[pygame.K_UP]:
        game.speed_up_front()
    elif keys[pygame.K_SPACE]:
        game.brake()
    elif keys[pygame.K_DOWN]:
        game.speed_up_reverse()

    game.draw()
    game.next_frame()
    pygame.display.update()
    clock.tick(60)