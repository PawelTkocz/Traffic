import pygame
import Car
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1400, 800))
clock = pygame.time.Clock()

c = Car.Car(100, 180, 700, 200)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        c.turn(0.05, -1)
    elif keys[pygame.K_RIGHT]:
        c.turn(0.05, 1)
    if keys[pygame.K_UP]:
        c.vel += 0.1
    elif keys[pygame.K_DOWN]:
        c.vel -= 0.1
    screen.fill("darkgray")
    c.draw(screen)
    c.move()
    pygame.display.update()
    clock.tick(60)