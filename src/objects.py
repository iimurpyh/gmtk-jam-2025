import pygame
import math
import os
from pygame.locals import *
import src.utils as utils
import pytmx
from pygame.locals import *
from src.tilemap import tilemap, collisionRects

RED = (255,0,0)

def loadImageStates(pathName):
    images = {}
    for file in os.listdir(pathName):
        if not os.path.isdir(file):
            print(os.path.basename(file))
            images[os.path.splitext(os.path.basename(file))[0]] = pygame.image.load(os.path.join(pathName, file))
    
    return images

class GameObject(pygame.sprite.Sprite):
    gameObjects = []


    def isTouchingWall(self):
        return self.rect.collidelist(collisionRects) != -1

    def __init__(self):
        super().__init__()
        GameObject.gameObjects.append(self)
        self.flipped = False
        self.image_offset = (0, 0)
    
    def draw(self, surface, camera_position):
        drawRect = pygame.Rect(self.rect.x + camera_position[0], self.rect.y + camera_position[1], self.rect.width, self.rect.height)
        #pygame.draw.rect(surface, (0, 0, 0), drawRect)
        if self.image:
            flipped = pygame.transform.flip(self.image, self.flipped, False)
            surface.blit(flipped, (drawRect.x + self.image_offset[0], drawRect.y + self.image_offset[1]))

    def update(self, dt):
        pass

    def delete(self):
        GameObject.gameObjects.remove(self)

class Boss(GameObject):

    def __init__(self, spawnPos):

        
        super().__init__()

        self.image = pygame.Surface([100,100])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        self.rect.x = spawnPos[0]
        self.rect.y = spawnPos[1]

        self.lastAttackTime = 0
        

        self.xVel = 0
        self.yVel = 0

    def circularProjectileAttack(self, qty, magnitude, spawnDist):
        for i in range(qty):
            projectile_angle = (360/qty) * i
            projectile_angle_radians = projectile_angle * (math.pi/180)
            spawnPosX = self.rect.x + spawnDist * math.sin(projectile_angle_radians)
            spawnPosY = self.rect.y + spawnDist * math.cos(projectile_angle_radians)
            Projectile(magnitude, projectile_angle, (spawnPosX, spawnPosY), False)

    def update(self, dt):
        if (pygame.time.get_ticks() - self.lastAttackTime) > 5000:
            self.circularProjectileAttack(5, 300, 20)
            self.lastAttackTime = pygame.time.get_ticks()


            

class Projectile(GameObject):
    def __init__(self, magnitude, direction, pos, isBouncy):

        super().__init__()

        self.image = pygame.Surface([50,50])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.isBouncy = isBouncy
        

        self.directionRadians = direction * (math.pi / 180.0)
        self.xVel = magnitude * math.sin(self.directionRadians)
        self.yVel = magnitude * math.cos(self.directionRadians)

    def update(self, dt):
        self.rect.x += self.xVel * dt
        self.rect.y += self.yVel * dt

        if self.isTouchingWall() and not self.isBouncy:
            self.delete()

class Player(GameObject):
    SPEED = 400

    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 130, 100)
        self.xVel = 0
        self.yVel = 0

        self.imageStates = loadImageStates("assets/cowboy")
        self.state = 'idle'

        self.lassoCharge = 0
        
        self.image_offset = (-40, -70)
    
    def handleMovement(self, dt):
        keys = pygame.key.get_pressed()

        if keys[K_UP]:
            self.yVel = -Player.SPEED
        elif keys[K_DOWN]:
            self.yVel = Player.SPEED
        else:
            self.yVel = 0

        if keys[K_LEFT]:
            self.flipped = False
            self.image_offset = (-40, -70)
            self.xVel = -Player.SPEED
        elif keys[K_RIGHT]:
            self.flipped = True
            self.image_offset = (-80, -70)
            self.xVel = Player.SPEED
        else:
            self.xVel = 0
        
        self.rect.x += self.xVel * dt
        if self.isTouchingWall():
            self.rect.x -= self.xVel * dt
            self.xVel = 0
            
        self.rect.y += self.yVel * dt
        if self.isTouchingWall():
            self.rect.y -= self.yVel * dt
            self.yVel = 0
    
    def handleLassoState(self, dt):
        if pygame.mouse.get_pressed()[0]:
            if self.state == 'idle':
                self.state = 'chargeLasso'
            if self.state == 'chargeLasso':
                if self.lassoCharge < 1:
                    self.lassoCharge += dt
        else:
            if self.state == 'chargeLasso':
                self.state = 'throwLasso'
                self.lassoCharge = 0

    def update(self, dt):
        self.image = self.imageStates[self.state]
        
        self.handleMovement(dt)
        self.handleLassoState(dt)

        
    
    def draw(self, surface, camera_position):
        start_pos = (self.rect.x + camera_position[0] + self.rect.width/2, self.rect.y + camera_position[1] + 40)
        mouse_pos = pygame.mouse.get_pos()
        translated = ((mouse_pos[0]*2) - start_pos[0], (mouse_pos[1]*2) - start_pos[1])
        end_pos = (translated[0]*self.lassoCharge + start_pos[0], translated[1]*self.lassoCharge + start_pos[1])

        if self.state == 'chargeLasso':
            utils.draw_line_round_corners_polygon(surface, start_pos, end_pos, (255, 255, 255), 20)
        
        super().draw(surface, camera_position)
        