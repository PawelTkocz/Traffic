import pygame
import Car
import CarFactory
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1400, 800))
clock = pygame.time.Clock()
car_factory = CarFactory.CarFactory()
c = car_factory.get_car(100, 180, 700, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        c.turn_left()
    elif keys[pygame.K_RIGHT]:
        c.turn_right()
    if keys[pygame.K_UP]:
        c.speed_up_front()
    elif keys[pygame.K_SPACE]:
        c.brake()
    elif keys[pygame.K_DOWN]:
        c.speed_up_reverse()
    screen.fill("darkgray")
    c.draw(screen)
    c.move()
    pygame.display.update()
    clock.tick(60)