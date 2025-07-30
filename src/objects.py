import pygame
from pygame.locals import *
import src.utils as utils

class GameObject(pygame.sprite.Sprite):
    gameObjects = []

    def isTouchingWall():
        

    def __init__(self):
        super().__init__()
        GameObject.gameObjects.append(self)

    def draw(self, surface, camera_position):
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(self.rect.x + camera_position[0], self.rect.y + camera_position[1], self.rect.width, self.rect.height))

class Player(GameObject):
    SPEED = 400

    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 70, 50)
        self.xv = 0
        self.yv = 0

    def update(self, dt):
        self.rect.x += self.xv * dt
        self.rect.y += self.yv * dt
        
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


