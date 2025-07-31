camera_position = (0, 0)
scale_factor = 2

def worldToScreenSpace(x, y):
    return (x + camera_position[0], y + camera_position[1])

def mouseToWorldSpace(pos):
    return (pos[0] * 2, pos[1] * 2)