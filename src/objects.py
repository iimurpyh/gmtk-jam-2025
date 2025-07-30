import pygame
from pygame.locals import *

class GameObject(pygame.sprite.Sprite):
    gameObjects = []

    def __init__(self, rect):
        GameObject.gameObjects.append(self)
        self.rect = rect
    
    def draw(self, surface):
        pass

    def update(self, dt):
        pass