import sys

import pygame
from pygame.locals import *

import engine

########################## HEADERS ##########################

# Game Setup
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 360
SQ_SIZE = 60
DIMENSION_X = 5
DIMENSION_Y = 6
FPS = 60

# BG color
BACKGROUND = (122, 255, 255)
BOARD_COLOR_A = pygame.Color('white')
BOARD_COLOR_B = pygame.Color('light grey')
HOVER_COLOR = (210, 140, 80)


########################## PROCESS FUNCTIONS ##########################


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
    for row in range(0, DIMENSION_Y):
        for col in range(0, DIMENSION_X):
            rectangle = pygame.Rect(
                col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)

            # Check if mouse is hovering
            if rectangle.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(WINDOW, HOVER_COLOR, rectangle)

            elif (row + col) % 2 == 0:
                pygame.draw.rect(WINDOW, BOARD_COLOR_A, rectangle)
            else:
                pygame.draw.rect(WINDOW, BOARD_COLOR_B, rectangle)


def drawPieces(WINDOW, Board, IMAGES):

    for row in range(DIMENSION_X):
        for col in range(DIMENSION_Y):
            piece = Board[col][row]
            if piece != '--':
                WINDOW.blit(IMAGES[piece], pygame.Rect(
                    row*SQ_SIZE, col*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def main():

    # initialize pygame
    pygame.init()

    # Set Display
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Hello from Pygame')
    clock = pygame.time.Clock()

    # Set GameState
    GAME_STATE = engine.GameState()
    SELECTED_PIECE = None

    # The main game loop
    running = True
    while running:
        # render game elements
        WINDOW.fill(BACKGROUND)
        clock.tick(FPS)

        ### PROCESS ###
        drawGameState(WINDOW, GAME_STATE)

        # Draw red border if a piece is selected
        if SELECTED_PIECE is not None:
            SELECTED_RECT = pygame.Rect(
                SELECTED_PIECE[0] * SQ_SIZE, SELECTED_PIECE[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(WINDOW, pygame.Color('red'), SELECTED_RECT, 3)

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x_coord = event.pos[0] // SQ_SIZE
                y_coord = event.pos[1] // SQ_SIZE

                SELECTED_PIECE = (x_coord, y_coord)

        # Update the window state
        pygame.display.update()


if __name__ == '__main__':
    main()
