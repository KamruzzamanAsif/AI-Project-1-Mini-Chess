import sys

import pygame
from pygame.locals import *

import engine

pygame.init()

########################## HEADERS ##########################

# Game Setup
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 450
SQ_SIZE = 60
DIMENSION_X = 5
DIMENSION_Y = 6
FPS = 60

# BG color
BACKGROUND = pygame.Color('azure')
BOARD_COLOR_A = pygame.Color('antiquewhite')
BOARD_COLOR_B = pygame.Color('darkseagreen4')
HOVER_COLOR = (210, 140, 80)

# Button colors
PLAY_BUTTON_COLOR = pygame.Color('chartreuse4')
RESTART_BUTTON_COLOR = pygame.Color('crimson')
BUTTON_TEXT_COLOR = pygame.Color('white')


# Button dimensions and positions
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 40
PLAY_BUTTON_POS = (40, 380)
RESTART_BUTTON_POS = (180, 380)

# Define button fonts
BUTTON_FONT = pygame.font.SysFont('Arial', 20, bold=True)


########################## PROCESS FUNCTIONS ##########################


def loadImages():

    IMAGES = {}
    pieces = ['b_B', 'b_K', 'b_N', 'b_P', 'b_Q', 'b_R',
              'w_B', 'w_K', 'w_N', 'w_P', 'w_Q', 'w_R']

    for piece in pieces:
        image = pygame.image.load('images/' + piece + '.png')
        IMAGES[piece] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))

    return IMAGES


def drawGameState(WINDOW, GAME_STATE, VALID_POS):
    images = loadImages()
    drawBoard(WINDOW)
    drawPieces(WINDOW, GAME_STATE.board, images)
    # mark_valid_pos(WINDOW, VALID_POS)
    drawButtons(WINDOW)


def drawBoard(WINDOW):

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # ADD SHAPES
    for row in range(0, DIMENSION_Y):
        for col in range(0, DIMENSION_X):
            rectangle = pygame.Rect(
                col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)

            # Calculate rank value for the current row
            rank = 6 - row

            # Calculate file value for the current column
            file_ = chr(ord('a') + col)

            # Check if mouse is hovering
            if rectangle.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(WINDOW, HOVER_COLOR, rectangle)
            elif (row + col) % 2 == 0:
                pygame.draw.rect(WINDOW, BOARD_COLOR_A, rectangle)
            else:
                pygame.draw.rect(WINDOW, BOARD_COLOR_B, rectangle)

            # Render rank value in the left cells
            if col == 0:
                font = pygame.font.SysFont('Comic Sans', 15)
                surface = font.render(str(rank), True, 'blue')
                WINDOW.blit(surface, (5, row * SQ_SIZE + 5))

            # Render file value in the bottom row
            if row == DIMENSION_Y - 1:
                font = pygame.font.SysFont('Comic Sans', 15)
                surface = font.render(file_, True, 'blue')
                WINDOW.blit(surface, (col * SQ_SIZE + 53,
                            (DIMENSION_Y-1) * SQ_SIZE + 45))


def drawPieces(WINDOW, Board, IMAGES):

    for row in range(DIMENSION_X):
        for col in range(DIMENSION_Y):
            piece = Board[col][row]
            if piece != '--':
                WINDOW.blit(IMAGES[piece], pygame.Rect(
                    row*SQ_SIZE, col*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawButtons(WINDOW):
    # Draw "Play" button
    play_button_rect = pygame.Rect(
        PLAY_BUTTON_POS[0], PLAY_BUTTON_POS[1], BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(WINDOW, PLAY_BUTTON_COLOR, play_button_rect)

    play_text = BUTTON_FONT.render("Play", True, BUTTON_TEXT_COLOR)
    play_text_rect = play_text.get_rect(center=play_button_rect.center)
    WINDOW.blit(play_text, play_text_rect)

    # Draw "Restart" button
    restart_button_rect = pygame.Rect(
        RESTART_BUTTON_POS[0], RESTART_BUTTON_POS[1], BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(WINDOW, RESTART_BUTTON_COLOR, restart_button_rect)

    restart_text = BUTTON_FONT.render("Restart", True, BUTTON_TEXT_COLOR)
    restart_text_rect = restart_text.get_rect(
        center=restart_button_rect.center)
    WINDOW.blit(restart_text, restart_text_rect)


def mark_valid_pos(WINDOW, VALID_POS):

    for position in VALID_POS:
        valid_rect = pygame.Rect(
            position[0] * SQ_SIZE, position[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(WINDOW, pygame.Color('red'), valid_rect, 3)


########################## MAIN FUNCTION ##########################


def main():

    # initialize pygame
    pygame.init()
    valid_positions = []
    pieceClickCount = 0
    selectedSq = []

    # Set Display
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Hello from Pygame')
    clock = pygame.time.Clock()

    # Set GameState
    GAME_STATE = engine.GameState()
    SELECTED_PIECE = None

    # Define the board area rect
    board_rect = pygame.Rect(
        0, 0, DIMENSION_X * SQ_SIZE, DIMENSION_Y * SQ_SIZE)

    # Button Rectengulars
    play_button_rect = pygame.Rect(
        PLAY_BUTTON_POS[0], PLAY_BUTTON_POS[1], BUTTON_WIDTH, BUTTON_HEIGHT)
    restart_button_rect = pygame.Rect(
        RESTART_BUTTON_POS[0], RESTART_BUTTON_POS[1], BUTTON_WIDTH, BUTTON_HEIGHT)

    # Get valid moves
    validMoves = GAME_STATE.getValidMoves()
    moveMade = False  # flag variable when a move is made

    # The main game loop
    running = True
    while running:

        # render game elements
        WINDOW.fill(BACKGROUND)
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if board_rect.collidepoint(event.pos):
                    y_coord = event.pos[0] // SQ_SIZE
                    x_coord = event.pos[1] // SQ_SIZE
                    selectedSq.append((x_coord, y_coord))

                    # mark selected piece
                    SELECTED_PIECE = (y_coord, x_coord)
                    pieceClickCount += 1

                # Check if "Play" button is clicked
                if play_button_rect.collidepoint(event.pos):
                    print("Play button pressed")

                # Check if "Restart" button is clicked
                if restart_button_rect.collidepoint(event.pos):
                    print("Restart button pressed")
                    GAME_STATE.undoMove('all')
                    moveMade = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:  # undo when z is pressed
                    GAME_STATE.undoMove()
                    moveMade = True

        # update valid moves
        if moveMade:
            validMoves = GAME_STATE.getValidMoves()
            moveMade = False

        # Set Game State
        drawGameState(WINDOW, GAME_STATE, valid_positions)

        # define piece movement
        if pieceClickCount == 2:

            move = engine.Move(selectedSq[0], selectedSq[1], GAME_STATE.board)
            print(move.getChessNotation())

            # if move valid then make move
            if move in validMoves:
                GAME_STATE.makeMove(move)
                moveMade = True
                pieceClickCount = 0
                selectedSq = []
            else:
                pieceClickCount = 1
                selectedSq.remove(selectedSq[0])

        # Draw red border if a piece is selected
        if SELECTED_PIECE is not None and pieceClickCount == 1:
            SELECTED_RECT = pygame.Rect(
                SELECTED_PIECE[0] * SQ_SIZE, SELECTED_PIECE[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(WINDOW, pygame.Color('blue'), SELECTED_RECT, 3)

        # Update the window state
        pygame.display.update()


if __name__ == '__main__':
    main()
