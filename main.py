import pygame
from pygame.locals import *
import pytmx
import pytmx.util_pygame


pygame.init()
screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()

tilemap = pytmx.util_pygame.load_pygame("assets/arena_chicken.tmx")

background_surface = pygame.Surface((tilemap.width * tilemap.tilewidth, tilemap.height * tilemap.tileheight))

FPS = 60

def draw_tilemap():
    background_surface.fill((255, 255, 255))
    for layer in tilemap.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, image in layer.tiles():
                background_surface.blit(image, (x * tilemap.tilewidth, y * tilemap.tileheight))

running = True

while running:
    dt = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    draw_tilemap()

    screen.blit(background_surface, (0, 0))
    pygame.display.update()

pygame.quit()