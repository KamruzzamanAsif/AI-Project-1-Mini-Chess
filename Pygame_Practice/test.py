import sys

import pygame
from pygame.locals import *

pygame.init()

# Game Setup
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 480
SQ_SIZE = 80

# BG color
BACKGROUND = (122, 255, 255)
FULL_RED = (255, 0, 0)
FULL_BLUE = (0, 255, 0)
FULL_GREEN = (0, 0, 255)
BOARD_COLOR_A = (118, 150, 86)
BOARD_COLOR_B = (238, 238, 210)
HOVER_COLOR = (210, 140, 80)

# Set Window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Hello from Pygame')

# The main game loop
while True:

    # code to close the window
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # render game elements
    WINDOW.fill(BACKGROUND)

    # ADD SHAPES
    for row in range(0, 6):
        for col in range(0, 5):
            rectangle = pygame.Rect(
                col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)

            # Check if mouse is hovering
            if rectangle.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(WINDOW, HOVER_COLOR, rectangle)

            elif (row + col) % 2 == 0:
                pygame.draw.rect(WINDOW, BOARD_COLOR_A, rectangle)
            else:
                pygame.draw.rect(WINDOW, BOARD_COLOR_B, rectangle)

    # this is must to update the window state
    pygame.display.update()
