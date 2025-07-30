import pygame
import math
from pygame.locals import *
import src.utils as utils
import pytmx
from pygame.locals import *
from src.tilemap import tilemap, collisionRects

RED = (255,0,0)

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

class Boss(GameObject):

    def __init__(self):

        
        super().__init__()

        self.image = pygame.Surface([100,100])
        self.image.fill(RED)

        self.rect = pygame.image.get_rect()


        self.xVel = 0
        self.yVel = 0

    #def circularProjectileAttack(self, qty, projectile):

class Projectile(GameObject):
    def __init__(self, magnitude, direction, pos):

        super().__init__()

        self.image = pygame.Surface([50,50])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        

        self.directionRadians = direction * (math.pi / 180.0)
        self.xVel = magnitude * math.sin(self.directionRadians)
        self.yVel = magnitude * math.cos(self.directionRadians)

    def update(self, dt):
        self.rect.x += self.xVel * dt
        self.rect.y += self.yVel * dt


class Player(GameObject):
    SPEED = 400

    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 70, 50)
        self.xv = 0
        self.yv = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[K_UP]:
            self.yv = -Player.SPEED
        elif keys[K_DOWN]:
            self.yv = Player.SPEED
        else:
            self.yv = 0

        if keys[K_LEFT]:
            self.xv = -Player.SPEED
        elif keys[K_RIGHT]:
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