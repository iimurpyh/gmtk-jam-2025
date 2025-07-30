import pygame
from pygame.locals import *


RED = (255,0,0)

class GameObject(pygame.sprite.Sprite):
    gameObjects = []

    def __init__(self, rect):
        GameObject.gameObjects.append(self)
        self.rect = rect
    
    def draw(self, surface):
        pass

    def update(self, dt):
        pass

class Boss(GameObject):

    def __init__(self):


        self.image = pygame.Surface([100,100])
        self.image.fill(RED)

        self.rect = pygame.image.get_rect()

        super().__init__(self.rect)

        self.xVel = 0
        self.yVel = 0

    def circularProjectileAttack(self, qty, projectile):
        for i in range(qty):
            projectile

class Projectile(GameObject):
