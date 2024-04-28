import pygame
import Car
import CarFactory
from sys import exit

class ParallelParkingDemo:
    screen_height = 800
    screen_width = 1400
    def __init__(self):
        car_factory = CarFactory.CarFactory()
        self.car_lenght = 360
        self.car_width = 200
        offset_x = (self.screen_width - 3.5 * self.car_lenght) // 2
        offset_y = self.screen_height - 1.5 * self.car_width
        self.c1 = car_factory.get_car(self.car_width, self.car_lenght, offset_x + self.car_lenght, offset_y, [1, 0], color="#4287f5")
        self.c2 = car_factory.get_car(self.car_width, self.car_lenght, 0, 0, [1, 0], color="#e8e531")
        print(self.c2.corners)
        #self.c2 = car_factory.get_car(self.car_width, self.car_lenght, offset_x + 3.5 * self.car_lenght, offset_y, [1, 0], color="#e8e531")
        self.c3 = car_factory.get_car(self.car_width, self.car_lenght, offset_x, offset_y - 1.5*self.car_width, [1, 0], color="#b82f11")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.cur_phase = 0
        self.phases = [self.phase_zero, self.phase_one, self.phase_two, self.phase_three, self.phase_four, self.phase_five]

    def draw(self):
        self.screen.fill("darkgray")
        self.c1.draw(self.screen)
        self.c2.draw(self.screen)
        self.c3.draw(self.screen)

    def phase_zero(self):
        self.c3.speed_up_front()
        if self.c3.front_left[0] > self.c2.rear_left[0]:
            self.cur_phase += 1

    def phase_one(self):
        self.c3.brake()
        if self.c3.vel == 0:
            self.cur_phase += 1

    def phase_two(self):
        self.c3.turn_right()
        if self.c3.wheels.is_max_angle():
            self.cur_phase += 1

    def phase_three(self):
        self.c3.speed_up_reverse()
        if self.c3.rear_right[1] > self.c2.rear_left[1]:
            self.cur_phase += 1
    
    def phase_four(self):
        self.c3.vel = 0
        self.c3.turn_left()
        if self.c3.wheels.is_max_angle():
            self.cur_phase += 1

    def phase_five(self):
        self.c3.brake()

    def next_frame(self):
        self.phases[self.cur_phase]()
        self.c3.move()        
        self.draw()


pygame.init()
clock = pygame.time.Clock()
demo = ParallelParkingDemo()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    demo.draw()
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        demo.c3.turn_left()
    elif keys[pygame.K_RIGHT]:
        demo.c3.turn_right()
    if keys[pygame.K_UP]:
        demo.c3.speed_up_front()
    elif keys[pygame.K_SPACE]:
        demo.c3.brake()
    elif keys[pygame.K_DOWN]:
        demo.c3.speed_up_reverse()

    demo.next_frame()
    pygame.display.update()
    clock.tick(60)