import pygame, numpy as np
from itertools import cycle

block_size = 50
block_img =    {1: "asset/1.svg",
                2: "asset/2.svg",
                3: "asset/3.svg",
                4: "asset/4.svg",
                5: "asset/5.svg",
                6: "asset/6.svg",
                7: "asset/7.svg",
                8: "asset/8.svg",
                9: "asset/9.svg",}

class Block(object):
    def __init__(self, column, row, num):
        self.x = column
        self.y = row
        self.num = num
        self.dest = 0

def blink_block(screen, block, count, show):
    if count > 3:
        return
    count = 0
    time = pygame.time.get_ticks()
    if time % delay <= 20:
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(100, 200, 50, 50))
        show = not show
    if show:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(100, 200, 50, 50))
    blink_block(screen, block, count+1, show)

def draw_block(screen, block, color=False):
    sx = block.x*block_size
    sy = block.y*block_size
    image = pygame.image.load(block_img[block.num])
    if color:
        print("Blackening!")
        image.fill((0, 0, 0))
    screen.blit(image, pygame.Rect(sx, sy, block_size, block_size))

text_color = (255, 255, 255)

def main():

    clock = pygame.time.Clock()
    pygame.init()
    font = pygame.font.SysFont("arialblack", 20)
    width = 500
    height = 500
    block_size = 50
    block = Block(4, 0.5, 8)
    screen = pygame.display.set_mode((width, height))
    running, disappearing = True, True 
    count, delay = 0, 100
    blink_event = pygame.USEREVENT + 0

    current_time = pygame.time.get_ticks()
    change_time = current_time + delay
    show, start_screen = True, True

    logo = pygame.image.load("asset/logo.png").convert_alpha()
    logo = pygame.transform.scale(logo, (250, 250))
    background = pygame.image.load("asset/Gameover.png").convert_alpha()
    on_text_surface = font.render("Press any key to continue..", True, text_color)
    text_rect = on_text_surface.get_rect(center=(screen.get_width()/2, screen.get_height()/1.3))
    off_text_surface = pygame.Surface(text_rect.size)
    blink_surfaces = cycle([on_text_surface, off_text_surface])
    blink_surface = next(blink_surfaces)
    pygame.time.set_timer(blink_event, 1000)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == blink_event:
                blink_surface = next(blink_surfaces)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    start_screen = False
                    background = True
                    # disappearing = True 
        
        if background:
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))

        if start_screen:
            # screen.blit(logo, logo_rect, logo_rect.get_rect(center=(screen.get_width()/2, screen.get_height()/1.5)))
            screen.blit(logo, (screen.get_width()/4, screen.get_height()/5))
            screen.blit(blink_surface, text_rect)

        # current_time = pygame.time.get_ticks()
        # if disappearing:
        #     if count > 4:
        #         count = 0
        #         disappearing = False
        #         show = True 
        #         print("Finished!")
        #     if current_time >= change_time:
        #         change_time = current_time + delay 
        #         show = not show
        #         count += 1
        #         print("Hiding" if show else "Showing")
        #         print(count)
        #     draw_block(screen, block, True if show else False)

        pygame.display.flip()
        clock.tick(60)

main()

# def dropper(block):
#     while block.y < (height//block_size)-1:
#         block.y += speed
#         draw_window(screen, block)

# def event_handler():
#     if block.y > (block.dest):
#         block.dest = 0
#         block.y = block.dest
#     if block.dest:
#         block.y = float(block.y) +speed
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_a]:
#         block.x = np.clip(block.x-speed, 0, (width//block_size)-1)
#     if keys[pygame.K_w]:
#         block.y = np.clip(block.y-speed, 0, (height//block_size)-1)
#     if keys[pygame.K_s]:
#         block.dest = 5 
#     if keys[pygame.K_d]:
#         block.x = np.clip(block.x+speed, 0, (width//block_size)-1)

# if something:
#     draw_block(screen, block, (0, 0, 0))
# else:
#     draw_block(screen, block, (255, 0, 0))
# something = not something

