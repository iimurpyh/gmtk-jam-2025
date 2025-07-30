import pygame
import pytmx
import pytmx.util_pygame

tilemap = pytmx.util_pygame.load_pygame("assets/arena_chicken.tmx")

collisionRects = []

for layer in tilemap.visible_layers:
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, gid in layer.iter_data():
            if tilemap.get_tile_properties_by_gid(gid) and tilemap.get_tile_properties_by_gid(gid)['type'] == "solid":
                collisionRects.append(pygame.Rect(x * tilemap.tilewidth, y * tilemap.tileheight, tilemap.tilewidth, tilemap.tileheight))