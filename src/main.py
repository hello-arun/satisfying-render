import pygame
import pymunk
import pymunk.pygame_util
import math


pygame.init()

WIDTH, HEIGHT = 1024, 768

window = pygame.display.set_mode((WIDTH, HEIGHT))


def create_ball(space,radius,mass):
    body = pymunk.Body()
    body.position = (300,300)
    shape = pymunk.Circle(body,radius)
    shape.mass = mass
    shape.color = (255,0,0,100)
    space.add(body,shape)
    return shape

def draw(space,window,draw_options):
    window.fill("White")
    space.debug_draw(draw_options)
    pygame.display.update()

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps
    space = pymunk.Space()
    space.gravity = (0,98.7)
    ball = create_ball(space,10,25)
    draw_options = pymunk.pygame_util.DrawOptions(window)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(space,window,draw_options)
        space.step(dt)
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
