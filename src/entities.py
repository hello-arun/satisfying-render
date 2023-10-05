from pymunk import Body,Circle,Space,Segment
import pygame
from math import ceil

class Ball:
    def __init__(self,pos,radius) -> None:
        self.body:Body = Body()
        self.body.position = pos
        self.shape = Circle(self.body,radius)
        self.shape.friction = 0.0
        self.shape.elasticity = 0.9

    def addToSpace(self,space:Space):
        space.add(self.body,self.shape)

    def draw(self,screen):
        pass

    def debug(self):
        print("Position:",self.body.position,"self.shape.radius:",self.shape.radius)


class MovingBall(Ball):
    def __init__(self, pos, radius, mass=25, color=(0,255,0)) -> None:
        super().__init__(pos, radius)
        self.body.body_type=Body.DYNAMIC
        self.shape.mass = mass
        self.shape.color = color

    def draw(self, screen:pygame.Surface, camera):
        pos=self.body.position-camera.pos
        pygame.draw.circle(screen,self.shape.color,pos,self.shape.radius)

class StaticBall(Ball):
    def __init__(self, pos, radius, color=(255,0,0)) -> None:
        super().__init__(pos, radius)
        self.shape.color = color
        self.body.body_type=Body.STATIC
        self.shape.elasticity=0.6

    def draw(self, screen:pygame.Surface, camera):
        pos=self.body.position-camera.pos
        pygame.draw.circle(screen,self.shape.color,pos,self.shape.radius)


class Boundary:
    def __init__(self,start:pygame.Vector2,end:pygame.Vector2,thickness:int=2) -> None:
        self.segment = Segment(Space.static_body, (0, 0), (640, 0), thickness)
        self.segment.elasticity = 1
        self.segment.friction = 0
    
    def addToSpace(self,space):
        space.add(self.segment)

    def draw(self,space,camera):
        self.segment.a-camera.pos


class Camera:
    def __init__(self, pos,width,height):
        self.width=width
        self.height= height
        self.pos = 0,0
        self.lerp_factor=0.1
        # self.view = pygame.Rect(0, 0, width, height)     

    def update(self, target:MovingBall):
        tx,ty = target.body.position
        camx,camy=self.pos
        x = tx - int(self.width / 2)
        y = ty - int(self.height / 4)
        self.pos = camx + (x - camx) * self.lerp_factor, camy + (y - camy) * self.lerp_factor

        # Limit camera to stay within the game world boundaries (if needed)
        # x = min(0, x)
        # y = min(0, y)
        # x = max(0, x)
        # y = max(-(self.height - HEIGHT), y)

        # Smoothly move the camera towards the target position
        # self.camera_rect.x += (x - self.camera_rect.x) * self.lerp_factor
        # self.camera_rect.y += (y - self.camera_rect.y) * self.lerp_factor


        # tx, ty = target.body.position
        # x,y = self.pos 
            # tx
        # x = tX + int(self.width / 2)
        # y = -tY + int(self.height / 2)
        # self.pos = tx-500,ty-500

class Grid:
    def __init__(self,width, height, cell_size=32, color1=(100, 100, 100) , color2=(150, 150, 150) ) -> None:
        self.cell_size = cell_size
        self.width=cell_size*(ceil(width/cell_size)+8)
        self.height=cell_size*(ceil(height/cell_size)+8)
        self.grid_surface = pygame.Surface((width, height))
        self.color1, self.color2 = color1, color2
        
    def draw(self,screen,camera):
        camx,camy=camera.pos
        self.grid_surface.fill("white")
        shiftX=camx-int(camx/(2*self.cell_size))*2*self.cell_size
        shiftY=camy-int(camy/(2*self.cell_size))*2*self.cell_size
        for y in range(0, self.height, self.cell_size):
            for x in range(0, self.width, self.cell_size):
                pygame.draw.rect(
                    self.grid_surface,
                    self.color1 if (x // self.cell_size + y // self.cell_size) % 2 == 0 else self.color2,
                    (x-shiftX-2*self.cell_size, y-shiftY-2*self.cell_size, self.cell_size, self.cell_size),
                )
        screen.blit(self.grid_surface,(0,0))
