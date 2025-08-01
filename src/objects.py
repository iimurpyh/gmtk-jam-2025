import pygame
import math
import os
from pygame.locals import *
import src.utils as utils
import src.camera as camera
import pytmx
from pygame.locals import *
from src.tilemap import tilemap, collisionRects
import random


RED = (255,0,0)
ARENA_TOP = 120
ARENA_BOTTOM = 1100
ARENA_LEFT = 130
ARENA_RIGHT = 1400

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
    
    def draw(self, surface):
        drawPosition = camera.worldToScreenSpace(self.rect.x, self.rect.y)
        drawRect = pygame.Rect(drawPosition[0], drawPosition[1], self.rect.width, self.rect.height)
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

        self.state = 'idle'
        self.image_states = loadImageStates("assets/chicken")
        self.image_offsets = {}
        for key in self.image_states:
            if key == 'idle':
                self.image_offsets[key] = (0, 0)
            elif key == 'windup':
                self.image_offsets[key] = (25, -30)
            elif key == 'burst':
                self.image_offsets[key] = (-15, -25)
            else:
                self.image_offsets[key] = (0, 0)

        self.battleStage = 0
        self.alreadyAttacked = False

    def update(self, dt):
        player = self.getPlayer()

        playerDistX = player.getPos()[0] - self.rect.x
        playerDistY = player.getPos()[1] - self.rect.y

        playerAngle = math.atan2(playerDistX,playerDistY) * (180/math.pi)

        self.image = self.image_states[self.state]
        self.image_offset = self.image_offsets[self.state]

        if self.battleStage == 0:
            self.battleStage0(playerAngle)
        if self.battleStage == 1:
            self.battleStage1(playerAngle)
        if self.battleStage == 2:
            self.battleStage2(playerAngle)
        if self.battleStage == 3:
            self.battleStage3Transition(dt)
        if self.battleStage == 4:
            self.battleStage3(dt, playerAngle)


    def battleStage0(self, playerAngle):
        timeSinceLastAttack = pygame.time.get_ticks() - self.lastAttackTime
        if timeSinceLastAttack > 500:
            self.state = 'idle'
        if timeSinceLastAttack > 4500:
            self.state = 'windup'
        if timeSinceLastAttack > 5000:
            Projectile.targetedProjectileAttack(5, 400, 100, (self.rect.x, self.rect.y), False, playerAngle, 4, 10)
            self.lastAttackTime = pygame.time.get_ticks()
            self.health -= 10
            print(self.health)
            self.state = 'featherThrow'

        if self.health == 0:    
            self.battleStage += 1
            self.health = 100
            print("0th stage complete")

    def battleStage1(self, playerAngle):
        timeSinceLastAttack = pygame.time.get_ticks() - self.lastAttackTime
        if timeSinceLastAttack > 500:
            self.state = 'idle'
        if timeSinceLastAttack > 1500:
            self.state = 'windup'
        if timeSinceLastAttack > 2000:
            Projectile.circularProjectileAttack(10, 400, 100, (self.rect.x, self.rect.y), False, playerAngle, 4)
            self.lastAttackTime = pygame.time.get_ticks()
            self.health -= 10
            print(self.health)
            self.state = 'burst'

        if self.health == 0:    
            self.battleStage += 1
            self.health = 100
            print("1st stage complete")

    def battleStage2(self, playerAngle):
        timeSinceLastAttack = pygame.time.get_ticks() - self.lastAttackTime
        if timeSinceLastAttack > 500:
            self.state = 'idle'
        if timeSinceLastAttack > 2500:
            self.state = 'windup'
        if (pygame.time.get_ticks() - self.lastAttackTime) > 3000:
            Projectile.circularProjectileAttack(5, 400, 20, self.rect, True, playerAngle, 4)
            self.lastAttackTime = pygame.time.get_ticks()
            self.health -= 10
            print(self.health)
            self.state = 'burst'
        
        ''''
        if hit by rope:
            self.health -= 10
            print(self.health)
        '''''           

        if self.health == 0:
            self.battleStage += 1
            print("2nd stage complete")
            self.lastAttackTime = pygame.time.get_ticks()

    def battleStage3Transition(self,dt):
        if self.rect.y > ARENA_TOP + 100:
            self.rect.y -= 100 * dt
            self.state = 'fly'
        else:
            self.battleStage += 1
            self.alreadyAttacked = True

    def battleStage3(self, dt, playerAngle):

        self.state = 'fly2'

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

        image = pygame.image.load('assets/feather.png', 'feather')
        imageScaled = pygame.transform.scale(image, (40,80))
        imageRotated = pygame.transform.rotate(imageScaled, direction)
        self.image = imageRotated

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

    def targetedProjectileAttack(qty, magnitude, spawnDist, origin, isBouncy, initialAngle, bounceLimit, spreadAngle):
        prevAngle = 0
        for i in range(qty):
            multiplier = 1
            if i % 2 == 0:
                multiplier = -1
            prevAngle = prevAngle + spreadAngle * i * multiplier
            projectile_angle = initialAngle + prevAngle
            projectile_angle_radians = projectile_angle * (math.pi/180)
            spawnPosX = origin[0] + spawnDist * math.sin(projectile_angle_radians)
            spawnPosY = origin[1] + spawnDist * math.cos(projectile_angle_radians)
            Projectile(magnitude, projectile_angle, (spawnPosX, spawnPosY), isBouncy, bounceLimit)


        
            
class ThrownLasso(GameObject):
    def __init__(self, thrower, xVel, yVel, lastTime):
        super().__init__()
        self.rect = pygame.Rect(thrower.rect.x, thrower.rect.y, 48, 10)
        self.image = pygame.image.load('assets/thrownLasso.png', 'thrownLasso')

        self.xVel = xVel
        self.yVel = yVel
        self.thrower = thrower
        self.lastTime = lastTime

    def update(self, dt):
        self.rect.x += self.xVel * dt
        self.rect.y += self.yVel * dt
        self.lastTime -= dt

        if self.lastTime < 0:
            self.xVel += (self.thrower.rect.x - self.rect.x) * (0.3 + self.lastTime * 0.01)
            self.yVel += (self.thrower.rect.y - self.rect.y) * (0.3 + self.lastTime * 0.01)

            if self.rect.colliderect(self.thrower.rect):
                self.delete()
                self.thrower.state = 'idle'
            
            pos = pygame.math.Vector2(self.rect.x, self.rect.y)
            pos = pos.move_towards(pygame.math.Vector2(self.thrower.rect.x, self.thrower.rect.y), -self.lastTime*30)
            self.rect.x = pos.x
            self.rect.y = pos.y
    

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
    
    def handle_movement(self, dt):
        keys = pygame.key.get_pressed()

        if keys[K_UP] or keys[K_w]:
            self.yVel = -Player.SPEED
        elif keys[K_DOWN] or keys[K_s]:
            self.yVel = Player.SPEED
        else:
            self.yVel = 0

        if keys[K_LEFT] or keys[K_a]:
            self.flipped = False
            self.image_offset = (-40, -70)
            self.xVel = -Player.SPEED
        elif keys[K_RIGHT] or keys[K_d]:
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
    
    def throw_lasso(self):
        mouse_pos = pygame.mouse.get_pos()
        throw_speed = pygame.math.Vector2(mouse_pos[0] - 450, mouse_pos[1] - 450)
        throw_speed.scale_to_length(600 + (self.lassoCharge * 600))

        ThrownLasso(self, throw_speed.x, throw_speed.y, self.lassoCharge/2)

        self.lassoCharge = 0

    
    def handle_lasso(self, dt):
        if pygame.mouse.get_pressed()[0]:
            if self.state == 'idle':
                self.state = 'chargeLasso'
            if self.state == 'chargeLasso':
                if self.lassoCharge < 1:
                    self.lassoCharge += dt
        else:
            if self.state == 'chargeLasso':
                self.throw_lasso()
                self.state = 'throwLasso'

    def update(self, dt):
        self.image = self.imageStates[self.state]
        
        self.handle_movement(dt)
        self.handle_lasso(dt)
    
    def draw(self, surface):
        if self.state == 'chargeLasso' and self.lassoCharge > 0:
            start_pos = camera.worldToScreenSpace(self.rect.x + self.rect.width/2, self.rect.y + 40)
            mouse_pos = camera.mouseToWorldSpace(pygame.mouse.get_pos())
            end_pos = pygame.math.Vector2((mouse_pos[0] - start_pos[0]), (mouse_pos[1] - start_pos[1]))
            end_pos.scale_to_length(self.lassoCharge * 500)
            utils.draw_line_round_corners_polygon(surface, start_pos, (end_pos.x + start_pos[0], end_pos.y + start_pos[1]), (255, 255, 255), 20)
        
        super().draw(surface)

    def getPos(self):
        return (self.rect.x, self.rect.y)
        