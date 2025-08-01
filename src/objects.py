import pygame
import math
from pygame.locals import *
import src.utils as utils
import pytmx
from pygame.locals import *
from src.tilemap import tilemap, collisionRects
import random

RED = (255,0,0)
ARENA_TOP = 120
ARENA_BOTTOM = 1100
ARENA_LEFT = 130
ARENA_RIGHT = 1400

class GameObject(pygame.sprite.Sprite):
    gameObjects = []

    def isTouchingWall(self):
        return self.rect.collidelist(collisionRects) != -1

    def __init__(self):
        super().__init__()
        GameObject.gameObjects.append(self)
    
    def draw(self, surface, camera_position):
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(self.rect.x + camera_position[0], self.rect.y + camera_position[1], self.rect.width, self.rect.height))

    def update(self, dt):
        pass

    def delete(self):
        GameObject.gameObjects.remove(self)

class Boss(GameObject):

    def __init__(self, spawnPos):

        
        super().__init__()

        self.image = pygame.Surface([100,100])
        self.image.fill(RED)

        self.health = 100

        self.rect = self.image.get_rect()

        self.rect.x = spawnPos[0]
        self.rect.y = spawnPos[1]

        self.lastAttackTime = 0

        self.xVel = 0
        self.yVel = 0

    def getPlayer(self):
        for object in GameObject.gameObjects:
            if isinstance(object,Player):
                return object
            
        return Player()



class ChickenBoss(Boss):


    FLYBY_SPEED = 1000

    def __init__(self, spawnPos):

        super().__init__(spawnPos)

        self.battleStage = 1
        self.alreadyAttacked = False

    def update(self, dt):
        player = self.getPlayer()

        playerDistX = player.getPos()[0] - self.rect.x
        playerDistY = player.getPos()[1] - self.rect.y

        playerAngle = math.atan2(playerDistX,playerDistY) * (180/math.pi)

        if self.battleStage == 1:
            self.battleStage1(playerAngle)
        if self.battleStage == 2:
            self.battleStage2(playerAngle)
        if self.battleStage == 3:
            self.battleStage3(dt, playerAngle)


    def battleStage1(self, playerAngle):
        if (pygame.time.get_ticks() - self.lastAttackTime) > 2000:
            Projectile.circularProjectileAttack(10, 400, 100, (self.rect.x, self.rect.y), False, playerAngle, 4)
            self.lastAttackTime = pygame.time.get_ticks()
            self.health -= 10
            print(self.health)

        if self.health == 0:    
            self.battleStage += 1
            self.health = 100
            print("1st stage complete")

    def battleStage2(self, playerAngle):
        if (pygame.time.get_ticks() - self.lastAttackTime) > 3000:
            Projectile.circularProjectileAttack(5, 400, 20, self.rect, True, playerAngle, 4)
            self.lastAttackTime = pygame.time.get_ticks()
            self.health -= 10
            print(self.health)
        
        ''''
        if hit by rope:
            self.health -= 10
            print(self.health)
        '''''           

        if self.health == 0:
            self.battleStage += 1
            print("2nd stage complete")

    def battleStage3(self, dt, playerAngle):
        

        self.rect.x += ChickenBoss.FLYBY_SPEED * dt

        if self.rect.x > (ARENA_LEFT+ARENA_RIGHT)/2 and not self.alreadyAttacked:
            Projectile.circularProjectileAttack(10, 400, 20, self.rect, False, playerAngle, 4)
            self.alreadyAttacked = True
        
        if self.rect.x > 3000:
            self.rect.x = -1000
            self.rect.y = random.randint(ARENA_TOP+50, ARENA_BOTTOM-50)
            #Projectile.circularProjectileAttack(5, 400, 20, self.rect, True, playerAngle, 4)
            self.lastAttackTime = pygame.time.get_ticks()
            self.health -= 10
            print(self.health)
            self.alreadyAttacked = False



        
class Projectile(GameObject):
    def __init__(self, magnitude, direction, pos, isBouncy, bounceLimit):

        super().__init__()

        self.image = pygame.Surface([50,50])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.isBouncy = isBouncy
        self.numBounces = 0
        self.bounceLimit = bounceLimit

        self.directionRadians = direction * (math.pi / 180.0)
        self.xVel = magnitude * math.sin(self.directionRadians)
        self.yVel = magnitude * math.cos(self.directionRadians)

    def update(self, dt):
        self.rect.x += self.xVel * dt
        self.rect.y += self.yVel * dt

        if self.isTouchingWall():
            if not self.isBouncy:
                self.delete()
                
            #Kinda hacky but oh well
            if self.isBouncy and self.numBounces < self.bounceLimit:
                self.numBounces += 1
                if self.rect.y > ARENA_BOTTOM:
                    self.yVel *= -1
                    self.rect.y = ARENA_BOTTOM-1
                if self.rect.y < ARENA_TOP:
                    self.yVel *= -1
                    self.rect.y = ARENA_TOP+1
                if self.rect.x < ARENA_LEFT:
                    self.xVel *= -1
                    self.rect.x = ARENA_LEFT+1
                if self.rect.x > ARENA_RIGHT:
                    self.xVel *= -1
                    self.rect.x = ARENA_RIGHT-1
            if self.isBouncy and self.numBounces == self.bounceLimit:
                self.delete()
    
    def circularProjectileAttack(qty, magnitude, spawnDist, origin, isBouncy, initialAngle, bounceLimit):
        for i in range(qty):
            projectile_angle = ((360/qty) * i) + initialAngle
            projectile_angle_radians = projectile_angle * (math.pi/180)
            spawnPosX = origin[0] + spawnDist * math.sin(projectile_angle_radians)
            spawnPosY = origin[1] + spawnDist * math.cos(projectile_angle_radians)
            Projectile(magnitude, projectile_angle, (spawnPosX, spawnPosY), isBouncy, bounceLimit)
        
            


class Player(GameObject):
    SPEED = 400

    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 70, 50)
        self.xv = 0
        self.yv = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[K_UP] or keys[K_w]:
            self.yv = -Player.SPEED
        elif keys[K_DOWN] or keys[K_s]:
            self.yv = Player.SPEED
        else:
            self.yv = 0

        if keys[K_LEFT] or keys[K_a]:
            self.xv = -Player.SPEED
        elif keys[K_RIGHT] or keys[K_d]:
            self.xv = Player.SPEED
        else:
            self.xv = 0
        
        self.rect.x += self.xv * dt
        if self.isTouchingWall():
            self.rect.x -= self.xv * dt
            self.xv = 0
            
        self.rect.y += self.yv * dt
        if self.isTouchingWall():
            self.rect.y -= self.yv * dt
            self.yv = 0

    def getPos(self):
        return (self.rect.x, self.rect.y)