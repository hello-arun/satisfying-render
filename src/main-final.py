import random
random.seed(0)
import pymunk, pymunk.pygame_util
from pymunk import Body,Circle,Shape,Space
import numpy as np
import pygame
from pygame.mixer import Sound
from entities import StaticBall,MovingBall,Camera,Grid
from helper import getStaticBodies


def run(scree, WIDTH, HEIGHT):
    # Simulation Clock Setting
    fps = 60
    dt = 1/fps
    clock = pygame.time.Clock()

    # BackGround Music 
    musicOffset = 2000
    musicFileName="../data/harry-potter-marble-music.mp3"
    musicOnsetsFile=musicFileName.replace(".mp3",".txt")
    music:Sound = Sound(musicFileName)
    onsetTimes  = (np.loadtxt(musicOnsetsFile)+musicOffset).tolist()
    musicPlaying = False

    # Physics World
    space = Space()
    space.gravity = 0,90

    # Camera Setup
    camera = Camera(pos=(0,0),width=WIDTH,height=HEIGHT)
    # draw_options = pymunk.pygame_util.DrawOptions(screen)
    
    
    # Create Space
    space = Space()
    space.gravity=0,200

    # Backgound Grid For Pygame
    grid = Grid(WIDTH,HEIGHT)

    # Add Ball to Space
    hero = MovingBall(pos=(200,200),radius=25)
    hero.body.user_data = "Hero"
    hero.body.velocity = 30,5
    hero.addToSpace(space)

    staticBodies = getStaticBodies(space,onsetTimes,hero.body.user_data,fps=fps,flatNess=2.5,randomNess=0)
    for staticBody in staticBodies:
        staticBody.addToSpace(space)
    run = True
    currTime=0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        if currTime>musicOffset and not musicPlaying:
            Sound.play(music)
            musicPlaying=True

        camera.update(hero)
        scree.fill("White")
        grid.draw(screen,camera)
        hero.draw(screen,camera)
        for sb in staticBodies:
            sb.draw(screen,camera)

        pygame.display.update()
        space.step(dt)
        clock.tick(fps)
        currTime+=clock.get_time()
    
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    np.random.seed(1010)
    WIDTH, HEIGHT = 600, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    run(screen, WIDTH, HEIGHT)
