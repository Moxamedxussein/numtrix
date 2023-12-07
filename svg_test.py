from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

import os

for entry in os.scandir('.'):
    if entry.is_file():
        if "svg" in entry.name:
            file = entry.name.split(".")
            drawing = svg2rlg(entry.name)
            renderPM.drawToFile(drawing, f"{file[0]}.png")
            # print(file[0], file[-1])

# import pygame
# pygame.init()
# screen = pygame.display.set_mode((400, 400))
# image = pygame.image.load("1.png")
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#         screen.blit(image, image.get_rect())
#         pygame.display.flip()


