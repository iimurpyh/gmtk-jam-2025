import pygame
import pytmx
from pygame.locals import *
pygame.init()

SCREEN_SIZE = (900, 900)
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
from src.tilemap import tilemap
import src.objects as objects
import src.camera as camera

game_surface = pygame.Surface((SCREEN_SIZE[0]*2, SCREEN_SIZE[1]*2))
background_surface = pygame.Surface((tilemap.width * tilemap.tilewidth, tilemap.height * tilemap.tileheight))

FPS = 60

player = objects.Player()
player.rect.x = SCREEN_SIZE[0] / 2 + player.rect.width/2
player.rect.y = SCREEN_SIZE[1] / 2 + player.rect.height/2


boss = objects.Boss((450,450))

def draw_tilemap():
    background_surface.fill((255, 255, 255))
    for layer in tilemap.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, image in layer.tiles():
                background_surface.blit(image, (x * tilemap.tilewidth, y * tilemap.tileheight))

def startGame():
    running = True

    while running:
        running = True

        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        for sprite in objects.GameObject.gameObjects:
            sprite.update(dt)
        
        draw_tilemap()

        game_surface.fill((255, 255, 255))

        camera.camera_position = (-player.rect.x + SCREEN_SIZE[0] - player.rect.width/2, -player.rect.y + SCREEN_SIZE[1] - player.rect.height/2)

        game_surface.blit(background_surface, camera.camera_position)

        for sprite in objects.GameObject.gameObjects:
            sprite.draw(game_surface)

        pygame.draw.circle(game_surface, (225, 0, 0), (SCREEN_SIZE[0], SCREEN_SIZE[1]), 20)
        
        pygame.transform.scale(game_surface, SCREEN_SIZE, screen)

        

        pygame.display.update()

startGame()

pygame.quit()