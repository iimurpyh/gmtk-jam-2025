import pygame
import pytmx
import pytmx.util_pygame
import src.objects as objects
from pygame.locals import *

SCREEN_SIZE = (900, 900)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

tilemap = pytmx.util_pygame.load_pygame("assets/arena_chicken.tmx")

background_surface = pygame.Surface((tilemap.width * tilemap.tilewidth, tilemap.height * tilemap.tileheight))

FPS = 60

player = objects.Player()
player.rect.x = SCREEN_SIZE[0] / 2 + player.rect.width/2
player.rect.y = SCREEN_SIZE[1] / 2 + player.rect.height/2

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

        camera_position = (-player.rect.x + SCREEN_SIZE[0]/2 - player.rect.width/2, -player.rect.y + SCREEN_SIZE[1]/2 - player.rect.height/2)

        screen.blit(background_surface, camera_position)

        for sprite in objects.GameObject.gameObjects:
            sprite.draw(screen, camera_position)

        pygame.display.update()

startGame()

pygame.quit()