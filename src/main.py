import pygame
import pymunk
import pymunk.pygame_util
import numpy as np


def create_ball(space,radius,mass):
    body = pymunk.Body()
    body.position = (300,300)
    shape = pymunk.Circle(body,radius)
    shape.mass = mass
    shape.color = (255,0,0,100)
    space.add(body,shape)
    shape.elasticity=1.0
    shape.friction=0.5
    return shape

def create_boundaries(space,width,height):
    rects = [
        [(width/2,height-10),(width,20)],
        [(width/2,10),(width,20)],
        [(10,height/2),(20,height)],
        [(width-10,height/2),(20,height)],
    ]
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position=pos
        shape = pymunk.Poly.create_box(body,size)
        shape.elasticity=0.50
        shape.friction=0.5
        space.add(body,shape)
        # return shape

def draw_world(space,window,draw_options):
    space.debug_draw(draw_options)


def run(screen, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 120
    dt = 1/fps
    space = pymunk.Space()
    space.gravity = (0,0)
    ball:pymunk.Shape = create_ball(space,10,25)
    create_boundaries(space,WIDTH,HEIGHT)
    music = pygame.mixer.Sound("../data/mario-marble-music.mp3")
    beatTimes=np.loadtxt("../data/mario-marble-music.txt").tolist()
    # boundary =
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    TIME=0
    pygame.mixer.Sound.play(music)
    font = pygame.font.SysFont(None, 48)
    idx=0
    img:pygame.Surface = font.render(f'{idx}', True, (0,0,255))
    impulseDir=[(-5000,0),(0,-5000),(5000,0),(0,5000)]
    velocityDir=[(-500,0),(0,-500),(500,0),(0,500)]
    # for th in np.random.rand(60)*np.pi*2:
        # velocityDir.append((500*np.cos(th),500*np.sin(th)))
    while run:
        if TIME>=beatTimes[0]:
            bd:pymunk.Body=ball.body
            bd._set_velocity(velocityDir[idx%len(velocityDir)])
            # bd.apply_impulse_at_local_point(impulseDir[idx%4])
            img:pygame.Surface = font.render(f'{idx}', True, (0,0,255))
            idx+=1
            beatTimes.pop(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        screen.fill("White")
        draw_world(space,screen,draw_options)
        screen.blit(img, (100, 100))
        pygame.display.update()

        space.step(dt)
        TIME+=clock.get_time()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 1024, 768
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    run(screen, WIDTH, HEIGHT)
