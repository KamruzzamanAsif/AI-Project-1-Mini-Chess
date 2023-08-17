import sys

import pygame
from pygame.locals import *

import engine

# Game Setup
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 360
SQ_SIZE = 60
DIMENSION_X = 6
DIMENSION_Y = 5
FPS = 60

# BG color
BACKGROUND = (122, 255, 255)
FULL_RED = (255, 0, 0)
FULL_BLUE = (0, 255, 0)
FULL_GREEN = (0, 0, 255)
BOARD_COLOR_A = (118, 150, 86)
BOARD_COLOR_B = (238, 238, 210)
HOVER_COLOR = (210, 140, 80)

## PROCESS FUNCTIONS ##


def loadImages():

    IMAGES = {}
    pieces = ['b_B', 'b_K', 'b_Kn', 'b_P', 'b_Q', 'b_R',
              'w_B', 'w_K', 'w_Kn', 'w_P', 'w_Q', 'w_R']

    for piece in pieces:
        image = pygame.image.load('images/' + piece + '.png')
        IMAGES[piece] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))

    return IMAGES


def drawGameState(WINDOW, GAME_STATE):
    images = loadImages()
    drawBoard(WINDOW)
    drawPieces(WINDOW, GAME_STATE.board, images)


def drawBoard(WINDOW):

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # ADD SHAPES
    for row in range(0, 6):
        for col in range(0, 5):
            rectangle = pygame.Rect(
                col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)

            # Check if mouse is hovering
            if rectangle.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(WINDOW, HOVER_COLOR, rectangle)

            elif (row + col) % 2 == 0:
                pygame.draw.rect(WINDOW, pygame.Color('white'), rectangle)
            else:
                pygame.draw.rect(WINDOW, pygame.Color('light grey'), rectangle)


def drawPieces(WINDOW, Board, IMAGES):

    for row in range(DIMENSION_Y):
        for col in range(DIMENSION_X):
            piece = Board[col][row]
            print("R: ", row, "Col: ", col, "Board: ", piece)
            if piece != '--':
                WINDOW.blit(IMAGES[piece], pygame.Rect(
                    row*SQ_SIZE, col*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def main():

    pygame.init()

    # Set Window
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Hello from Pygame')
    clock = pygame.time.Clock()
    GAME_STATE = engine.GameState()

    running = True
    # The main game loop
    while running:

        # code to close the window
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # render game elements
        WINDOW.fill(BACKGROUND)
        clock.tick(FPS)

        ### PROCESS ###
        drawGameState(WINDOW, GAME_STATE)

        # this is must to update the window state
        pygame.display.update()


if __name__ == '__main__':
    main()
