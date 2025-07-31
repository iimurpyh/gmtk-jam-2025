import pygame
import math

def clamp(n, small, large):
    return max(small, min(n, large))

# taken from https://stackoverflow.com/questions/70051590/draw-lines-with-round-edges-in-pygame
def draw_line_round_corners_polygon(surf, p1, p2, c, w):
    p1v = pygame.math.Vector2(p1)
    p2v = pygame.math.Vector2(p2)
    lv = (p2v - p1v).normalize()
    lnv = pygame.math.Vector2(-lv.y, lv.x) * w // 2
    pts = [p1v + lnv, p2v + lnv, p2v - lnv, p1v - lnv]
    pygame.draw.polygon(surf, c, pts)
    pygame.draw.circle(surf, c, p1, round(w / 2))
    pygame.draw.circle(surf, c, p2, round(w / 2))