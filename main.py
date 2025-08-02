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
player.rect.x = SCREEN_SIZE[0] + player.rect.width
player.rect.y = SCREEN_SIZE[1] / 2 + player.rect.height/2

WHITE = (255,255,255)
BLACK = (0,0,0)
BACKGROUND_COL = (193,151,112)

boss = objects.ChickenBoss((725,550))


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
        
        pygame.transform.scale(game_surface, SCREEN_SIZE, screen)

        

        pygame.display.update()

def titleScreen():
    status = 'running'

    
    font = pygame.font.Font('assets\Deadtoast.ttf', 128)
    title = font.render('Cowboy Game', True, BLACK)

    ctrLine = SCREEN_SIZE[0]/2 - 10

    title_x = ctrLine - title.get_size()[0]/2
    title_y = 100

    title_rect = title.get_rect(x=title_x,y=title_y)

    button_width = 250
    button_height = 125

    play_button_ctr = (ctrLine - (button_width/2) - 200, title_y + 550)
    quit_button_ctr = (ctrLine - (button_width/2) + 200, title_y + 550)

    play_button = objects.Button(play_button_ctr[0], play_button_ctr[1], button_width, button_height, WHITE, BLACK, 'Play', 100)
    quit_button = objects.Button(quit_button_ctr[0], quit_button_ctr[1], button_width, button_height, WHITE, BLACK, 'Quit', 100)


    font2 = pygame.font.Font('assets\Deadtoast.ttf', 64)
    backstory_txt = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec semper tempus augue eu gravida. Maecenas tempus feugiat eros non rutrum. Curabitur vitae porttitor risus, in ornare ante. Nunc erat arcu, imperdiet nec tristique ut, porta sed dui. Sed id urna justo. Aenean posuere libero massa, vel consectetur urna pharetra nec. Mauris facilisis tristique nulla ac finibus. Aliquam consequat lacinia libero, vitae dictum lorem tempor a. In nisi dui, dapibus a enim nec, lobortis finibus ante. Morbi id ligula odio. Vivamus ut lacus lacus. Duis commodo, mauris eu maximus faucibus, ipsum nunc gravida mi, facilisis malesuada leo dolor a nisi. '

    backstory_width = 300
    backstory_height = 200
    
    backstory_ctr = (ctrLine - (backstory_width/2), title_y + 250)
    backstory_rect = pygame.Rect(backstory_ctr[0],backstory_ctr[1],backstory_width,backstory_height)

    while status == 'running':
        for event in pygame.event.get():
            if event.type == QUIT:
                status = 'quit'

        mouse_pos = pygame. mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if play_button.is_pressed(mouse_pos, mouse_pressed):
            status = 'play'

        if quit_button.is_pressed(mouse_pos, mouse_pressed):
            status = 'quit'

        screen.fill(BACKGROUND_COL)
        screen.blit(title, title_rect)
        #drawText(screen,backstory_txt,BLACK,backstory_rect,font2)
        screen.blit(play_button.image, play_button.rect)
        screen.blit(quit_button.image, quit_button.rect)
        clock.tick(FPS)
        pygame.display.update()

    if status == 'quit':
        pygame.quit()
    elif status == 'play':
        startGame()

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text
            
titleScreen()

pygame.quit()