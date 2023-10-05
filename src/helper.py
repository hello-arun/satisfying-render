import numpy as np
from pymunk import Body
from typing import List
from entities import StaticBall,MovingBall,Space

def getRandomUnitVectorWithinAngle(vec, theta):
    angle = np.random.uniform(-theta, theta)
    unit_vec = vec / np.linalg.norm(vec)
    rot_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                           [np.sin(angle), np.cos(angle)]])
    return np.dot(rot_matrix, unit_vec)

def findHero(bodies:List[Body],tag):
    for body in bodies:
        if body.user_data == tag:
            # print(body.position)
            return body
    return None

def getStaticBodies(realSpace:Space,hitTimes:List, heroTag="Hero",fps=60,flatNess=3.5,randomNess=np.pi/8) -> List[StaticBall]:
    imgSpace = realSpace.copy()
    fps = fps
    dt = 1/fps
    currTime=0
    deflectionDirecion=np.array([flatNess,1])
    staticBodies=[]
    while len(hitTimes):
        nextHitTime = hitTimes[0]
        stepsBeforeCollision = int((nextHitTime-currTime)/(1000.0*dt))
        # spc_copy = space.copy()
        for i in range(stepsBeforeCollision):
            imgSpace.step(dt)
            currTime+=1000*dt
        
        heroBody = findHero(imgSpace.bodies,heroTag)
        heroShape = list(heroBody.shapes)[0]
        pos = heroBody.position
        print(pos)

        vel_i = heroBody.velocity

        vel_f_unit = getRandomUnitVectorWithinAngle(deflectionDirecion,randomNess)
        obstacleDir =vel_i- vel_f_unit*np.linalg.norm(vel_i)
        obstacleDirUnit = obstacleDir/np.linalg.norm(obstacleDir)
        staticBallRadius = np.random.randint(20,35)
        staticBallPos = pos+obstacleDirUnit*(1+staticBallRadius+heroShape.radius)
        sb = StaticBall(pos=staticBallPos,radius=staticBallRadius)
        sb.addToSpace(imgSpace)

        sb = StaticBall(pos=staticBallPos,radius=staticBallRadius)
        staticBodies.append(sb)
        deflectionDirecion[0]*=-1
        hitTimes.pop(0)
    return staticBodies