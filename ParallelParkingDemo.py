import pygame
import Car
import CarFactory
from sys import exit

class ParallelParkingDemo:
    screen_height = 800
    screen_width = 1400
    def __init__(self):
        self.car_factory = CarFactory.CarFactory()
        self.car_lenght = 360
        self.car_width = 200
        offset_x = (self.screen_width - 3.5 * self.car_lenght) // 2
        offset_y = self.screen_height - 1.5 * self.car_width
        self.c1 = self.car_factory.get_car(self.car_width, self.car_lenght, offset_x + self.car_lenght, offset_y, [1, 0], color="#4287f5")
        self.c2 = self.car_factory.get_car(self.car_width, self.car_lenght, offset_x + 3.5 * self.car_lenght, offset_y, [1, 0], color="#e8e531")
        #poczatek
        #self.c3 = car_factory.get_car(self.car_width, self.car_lenght, offset_x, offset_y - 1.5*self.car_width, [1, 0], color="#b82f11")
        #zaparkowany
        #self.c3 = car_factory.get_car(self.car_width, self.car_lenght, offset_x + 2.25 * self.car_lenght, offset_y, [1, 0], color="#b82f11")
        self.c3 = self.car_factory.get_car(self.car_width, self.car_lenght, 1320, 243, [1, 0], color="#b82f11")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.cur_phase = 0
        self.phases = [self.phase_zero, self.phase_one, self.phase_two, self.phase_three, 
                       self.phase_four, self.phase_five, self.phase_six, self.phase_seven,
                       self.phase_eight, self.phase_nine, self.phase_ten, self.restart]

    def draw(self):
        self.screen.fill("darkgray")
        self.c1.draw(self.screen)
        self.c2.draw(self.screen)
        self.c3.draw(self.screen)

    def phase_zero(self):
        self.cur_phase = 2
        self.phase_two()
        self.c3.speed_up_front(1)
        if self.c3.front_left_pos()[0] > self.c2.front_left_pos()[0]:
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
        self.c3.speed_up_reverse(-3)
        if self.c3.rear_right_pos()[1] > 500:
            self.cur_phase += 1
        #if self.c3.rear_right_pos()[1] > self.c2.rear_left_pos()[1]:
        #    self.cur_phase += 1
    
    def phase_four(self):
        self.c3.brake()
        self.c3.straighten_wheels()
        if self.c3.wheels.are_straight():
            self.cur_phase += 1

    def phase_five(self):
        if self.c3.vel == 0: return
        self.c3.speed_up_reverse(-2)
        if self.c3.rear_left_pos()[1] > self.c1.front_left_pos()[1] - 80:
            self.cur_phase += 1

    def phase_six(self):
        self.c3.brake()
        self.c3.turn_left()
        if self.c3.wheels.is_max_angle():
            self.cur_phase += 1

    def phase_seven(self):
        self.c3.speed_up_reverse(-2)
        if self.c3.rear_left_pos()[0] > self.c3.rear_right_pos()[0] - 7:
            self.cur_phase += 1

    def phase_eight(self):
        self.c3.brake()
        self.c3.straighten_wheels()
        if self.c3.wheels.are_straight():
            self.cur_phase += 1

    def phase_nine(self):
        self.c3.speed_up_front(2)
        if self.c3.rear_left_pos()[0] > self.screen_width /2 - self.car_lenght / 2 - 20:
            self.cur_phase += 1

    def phase_ten(self):
        self.c3.brake()
        if self.c3.vel == 0:
            self.time_cnt = 60
            self.cur_phase += 1
        
    def restart(self):
        self.time_cnt -= 1
        if self.time_cnt == 0:
            self.c3 = self.car_factory.get_car(self.car_width, self.car_lenght, 1320, 243, [1, 0], color="#b82f11")
            self.cur_phase = 0

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
    elif keys[pygame.K_0]:
        print(demo.c3.rear_left_pos(), demo.c3.rear_right_pos(), demo.c3.front_left_pos(), demo.c3.front_right_pos())

    demo.next_frame()
    #demo.c3.move()
    #demo.c3.draw(demo.screen)
    pygame.display.update()
    clock.tick(60)