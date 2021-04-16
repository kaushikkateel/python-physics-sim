import pygame, sys, random, math
import numpy as np
from pygame import mixer

pygame.init()
w,h = (1280,720)
monitor_size = [w,h]
screen = pygame.display.set_mode(monitor_size)
pygame.display.set_caption('Verlet')
clock = pygame.time.Clock()
gameRun = True

collision_factor = 0.9
gravity = 0.2

pop_sound = mixer.Sound("data/sound/pop.wav")
pop_sound.set_volume(0.1)



class point():
    def __init__(self, x, y, initial_velocity, color):
        self.x = x
        self.y = y
        self.oldx = x - initial_velocity
        self.oldy = y - initial_velocity
        self.color = color

def distance(a,b,c,d):
    return math.sqrt((a-b)**2 + (c-d)**2)

def resolve_collision(point1, point2):
    x1 = point1.x
    y1 = point1.y
    x2 = point2.x
    y2 = point2.y
    vx1 = point1.x - point1.oldx
    vy1 = point1.y - point1.oldy
    vx2 = point2.x - point2.oldx
    vy2 = point2.y - point2.oldy

    nx = x2-x1
    ny = y2-y1
    unx = nx/(math.sqrt(nx**2 +ny**2))
    uny = ny/(math.sqrt(nx**2 +ny**2))
    utx = -uny
    uty = unx

    v1n = unx * vx1 + uny * vy1
    v2n = unx * vx2 + uny * vy2

    v1t = utx * vx1 + uty * vy1
    v2t = utx * vx2 + uty * vy2

    v1ndash = (2*v2n)/2
    v2ndash = (2*v1n)/2

    v1xn = v1ndash * unx
    v1yn = v1ndash * uny
    v2xn = v2ndash * unx
    v2yn = v2ndash * uny

    v1xt = v1ndash * utx
    v1yt = v1ndash * uty
    v2xt = v2ndash * utx
    v2yt = v2ndash * uty

    finalvx1 = v1xn + v1xt
    finalvy1 = v1yn + v1yt
    finalvx2 = v2xn + v2xt
    finalvy2 = v2yn + v2yt

    return finalvx1, finalvx2, finalvy1, finalvy2


def collision_detect(point1, point2):
    print(point1.y, point2.y)
    dist = distance(point2.x, point1.x, point2.y, point1.y)
    print(dist)
    if dist <= 20 :
        return True
    return False

def update_points(points):
    for point in points:
        vx = point.x - point.oldx
        vy = point.y - point.oldy
        point.oldx = point.x
        point.oldy = point.y
        point.x += vx
        point.y += vy
        point.y += gravity
        
        if(point.x > w):
            point.x = w
            point.oldx = point.x + vx * collision_factor
            
        elif(point.x <0):
            point.x = 0
            point.oldx = point.x + vx * collision_factor
            
        if(point.y > h):
            point.y = h
            point.oldy = point.y + vy * collision_factor
            
        elif(point.y <0):
            point.y = 0
            point.oldy = point.y + vy * collision_factor
        
        for q in points:
            if q == point:
                continue
            elif collision_detect(point, q) :
                x1, x2, y1, y2 = resolve_collision(point, q)
                point.x += x1
                point.y += y1
                q.x += x2
                q.y += y2
        


def draw_points(points):
    for point in points:
        pygame.draw.circle(screen,point.color,(point.x, point.y),10,0)


points = []
points.append(point(100,100,5,list(np.random.choice(range(256), size=3))))
points.append(point(150,150,2,list(np.random.choice(range(256), size=3))))
points.append(point(200,200,7,list(np.random.choice(range(256), size=3))))
points.append(point(250,250,9,list(np.random.choice(range(256), size=3))))

while gameRun:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30,30,30))
    update_points(points)
    draw_points(points)
    pygame.display.update()
    clock.tick(120)