import pymunk, pymunk.pygame_util
from pymunk import Body,Circle,Shape,Space
import numpy as np
import pygame
from pygame.mixer import Sound



class Ball:
    def __init__(self,pos,radius,body_type=Body.STATIC,color = None) -> None:
        """
        pos: (x,y)
        width: 
        height: 
        angle: in radian
        """

        self.body:Body = Body(body_type=body_type)
        self.body.position = pos
        self.shape:Circle = Circle(self.body,radius)
        if body_type==Body.DYNAMIC:
            self.shape.mass = 25
        self.shape.friction = 0.1
        self.shape.elasticity = 1
        self.shape.color = color if color is not None else (255,255,0,100) if body_type==Body.STATIC else (255,0,0,100)
    
    def draw(self,screen):
        pygame.draw.circle(screen,self.shape.color,self.body.position,self.shape.radius)

    def debug(self):
        print("Position:",self.body.position,"self.shape.radius:",self.shape.radius)

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
        shape.elasticity=1.00
        shape.friction=0.0
        
        space.add(body,shape)
        # return shape

def draw_world(space,window,draw_options):
    space.debug_draw(draw_options)

def whenCollision(arbiter, space, data):
    print("Collided")
    return True
    # sys.exit()


def random_unit_vector_within_angle(vector, theta_radians):
    # Step 1: Normalize the input vector
    normalized_vector = vector / np.linalg.norm(vector)
    
    # Step 2: Generate a random angle within the range of -θ to +θ (in radians)
    random_angle = np.random.uniform(-theta_radians, theta_radians)
    
    # Step 3: Create a rotation matrix
    rotation_matrix = np.array([[np.cos(random_angle), -np.sin(random_angle)],
                                [np.sin(random_angle), np.cos(random_angle)]])
    
    # Step 4: Multiply the normalized vector by the rotation matrix to obtain the random unit vector
    random_unit_vector = np.dot(rotation_matrix, normalized_vector)
    return random_unit_vector

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        centerx,centery=target.body.position
        x = -centerx + int(self.width / 2)
        y = -centery + int(self.height / 2)

        # Add boundary logic here to check if the target has crossed a boundary
        # For example, you can use conditions like if target.rect.x > boundary_x:

        # Update camera position
        self.camera = pygame.Rect(x, y, self.width, self.height)

def run(scree, width, height):
    run = True
    fps = 60
    dt = 1/fps
    
    clock = pygame.time.Clock()
    space = Space()
    space.gravity = (0,98)
    camera = Camera(width, height)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    # Music Reference
    musicFileName="../data/harry-potter-marble-music.mp3"
    beatTimeFileName=musicFileName.replace(".mp3",".txt")
    music:Sound = Sound(musicFileName)
    beatTimes=np.loadtxt(beatTimeFileName).tolist()
    
    # Create Space

    # Add Ball to Space
    ballDynamic:Ball = Ball(pos=(width/2,height/3),radius=20,body_type=Body.DYNAMIC)
    ballDynamic.shape.collision_type=0
    ballDynamic.body.velocity=(250,0)
    space.add(ballDynamic.body,ballDynamic.shape)
    objects=[ballDynamic]
    create_boundaries(space,width,height)
    # ballStatic:Ball = Ball(pos=(200,400),radius=20,body_type=Body.STATIC)
    # ballStatic.shape.collision_type=1
    # space.add(ballStatic.body,ballStatic.shape)
    staticBall=None
    ch=space.add_collision_handler(0,1)
    ch.begin = whenCollision

    # Sound.play(music)
    playing=False
    timeOffset = 500
    TIME=0
    handeled=False

    while run and len(beatTimes)>1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        if timeOffset<TIME and not playing:
            Sound.play(music)
            playing=True
        nextHitTime=beatTimes[0]+timeOffset
        if TIME<=nextHitTime:
            if not handeled:
                # if staticBall is not None:
                    # space.remove(staticBall.shape,staticBall.body)
                    # objects.pop(-1)
                print("Next Hit at",nextHitTime/1000.0)
                hitTimeSec=(nextHitTime-TIME)/1000.0
                numFrames=int(hitTimeSec*fps)-1
                # freeTimeSteps=int((nextHitTime-TIME)/fps)-1
                print(numFrames)
                for i in range(numFrames):
                    space.step(dt)
                vel=ballDynamic.body.velocity
                print(vel)
                pos=ballDynamic.body.position
                dir=random_unit_vector_within_angle(vel,np.pi/5)
                staticRadius=np.random.randint(20,30)
                staticPos=pos+dir*(1+staticRadius+ballDynamic.shape.radius)
                staticBall=Ball(staticPos,staticRadius,Body.STATIC)
                # staticBall.debug()
                space.add(staticBall.body,staticBall.shape)
                objects.append(staticBall)
                for i in range(numFrames):
                    space.step(-dt)
                handeled=True
        if TIME>nextHitTime+50 and handeled:
            handeled=False
            beatTimes.pop(0)
            space.remove(staticBall.shape,staticBall.body)
            objects.pop(-1)

        scree.fill("White")
        
        # space.debug_draw(draw_options)
        for obj in objects:
            obj.draw(screen)
        pygame.display.update()
        space.step(dt)
        clock.tick(fps)
        TIME+=clock.get_time()
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    np.random.seed(1010)
    WIDTH, HEIGHT =600,600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    run(screen, WIDTH, HEIGHT)
