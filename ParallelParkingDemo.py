import pygame
import Car
import CarFactory
from sys import exit

class ParallelParkingDemo:
    screen_height = 800
    screen_width = 1400
    def __init__(self):
        self.car_factory = CarFactory.CarFactory()
        self.car_length = 360
        self.car_width = 200
        offset_x = (self.screen_width - 3.5 * self.car_length) // 2
        offset_y = self.screen_height - 1.5 * self.car_width
        self.c1 = self.car_factory.get_car(self.car_width, self.car_length, offset_x + self.car_length, offset_y, [1, 0], color="#4287f5")
        self.c2 = self.car_factory.get_car(self.car_width, self.car_length, offset_x + 3.5 * self.car_length, offset_y, [1, 0], color="#e8e531")
        self.c3 = self.car_factory.get_car(self.car_width, self.car_length, -100, 243, [1, 0], color="#b82f11")
        self.c4 = self.car_factory.get_car(self.car_width, self.car_length, -1000, -20, [1, 0], color="#a10539")
        self.c5 = self.car_factory.get_car(self.car_width, self.car_length, -100, -20, [1, 0], color="#47290f")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.cur_phase = 0
        self.phases = [self.phase_zero, self.phase_one, self.phase_two, self.phase_three, 
                       self.phase_four, self.phase_five, self.phase_six, self.phase_seven,
                       self.phase_eight, self.phase_nine, self.phase_ten, self.restart]

    def draw_dashed_line(self, line_len, line_width, space, offset_y):
        i = space // 2
        while i < self.screen_width:
            pygame.draw.rect(self.screen, "#c3dedd", pygame.Rect(i, offset_y, line_len, line_width))
            i += line_len + space

    def draw_side_line(self):
        self.draw_dashed_line(200, 25, 200, self.screen_height-200 - 2*self.car_width)

    def draw_center_line(self):
        self.draw_dashed_line(100, 50, 100, self.screen_height-140 - self.car_width)      

    def draw(self):
        self.screen.fill("#343536")
        pygame.draw.rect(self.screen, "#6e6362", pygame.Rect(0, self.screen_height-90, self.screen_width, 90))
        self.draw_side_line()
        self.draw_center_line()
        self.c1.draw(self.screen)
        self.c2.draw(self.screen)
        self.c3.draw(self.screen)
        self.c4.draw(self.screen)
        self.c5.draw(self.screen)

    def phase_zero(self):
        self.c4.speed_up_front()
        self.c3.speed_up_front(5)
        if self.c3.front_left_pos()[0] > self.c2.front_left_pos()[0] - self.car_length / 3:
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
    
    def phase_four(self):
        self.c3.brake()
        self.c3.straighten_wheels()
        if self.c3.wheels.are_straight():
            self.cur_phase += 1

    def phase_five(self):
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
        if self.c3.rear_left_pos()[0] > self.screen_width /2 - self.car_length / 2 - 20:
            self.cur_phase += 1

    def phase_ten(self):
        self.c3.brake()
        if self.c3.vel == 0:
            self.time_cnt = 60
            self.cur_phase += 1
        
    def restart(self):
        self.time_cnt -= 1
        if self.time_cnt == 0:
            self.c3 = self.car_factory.get_car(self.car_width, self.car_length, -100, 243, [1, 0], color="#b82f11")
            self.c4 = self.car_factory.get_car(self.car_width, self.car_length, -1000, -20, [1, 0], color="#a10539")
            self.c5 = self.car_factory.get_car(self.car_width, self.car_length, -100, -20, [1, 0], color="#47290f")
            self.cur_phase = 0

    def next_frame(self):
        self.phases[self.cur_phase]()
        self.c3.move() 
        if self.cur_phase >= 5:
            self.c5.speed_up_front() 
        self.c4.move()
        self.c5.move()      
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

    demo.next_frame()
    pygame.display.update()
    clock.tick(60)