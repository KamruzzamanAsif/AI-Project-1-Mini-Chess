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


def drawGameState(WINDOW, GAME_STATE, VALID_POS):
    images = loadImages()
    drawBoard(WINDOW)
    drawPieces(WINDOW, GAME_STATE.board, images)
    mark_valid_pos(WINDOW, VALID_POS)


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


def get_valid_moves(piece, position, BOARD):
    x, y = position
    valid_moves = []
    print(BOARD[y])

    if piece == 'b_R' or piece == 'w_R':
        print("inside")
        # Rook can move horizontally or vertically
        # Check horizontally to the right
        for i in range(x + 1, DIMENSION_X):
            if BOARD[y][i] == '--':
                valid_moves.append((i, y))
            else:
                break
        # Check horizontally to the left
        for i in range(x - 1, -1, -1):
            if BOARD[y][i] == '--':
                valid_moves.append((i, y))
            else:
                break
        # Check vertically downward
        for i in range(y + 1, DIMENSION_Y):
            if BOARD[i][x] == '--':
                valid_moves.append((x, i))
            else:
                break
        # Check vertically upward
        for i in range(y - 1, -1, -1):
            if BOARD[i][x] == '--':
                valid_moves.append((x, i))
            else:
                break

    elif piece == 'b_B' or piece == 'w_B':
        # Bishop can move diagonally
        # Check diagonally to the bottom-right
        for i, j in zip(range(x + 1, DIMENSION_X), range(y + 1, DIMENSION_Y)):
            if BOARD[j][i] == '--':
                valid_moves.append((i, j))
            else:
                break
        # Check diagonally to the bottom-left
        for i, j in zip(range(x - 1, -1, -1), range(y + 1, DIMENSION_Y)):
            if BOARD[j][i] == '--':
                valid_moves.append((i, j))
            else:
                break
        # Check diagonally to the top-right
        for i, j in zip(range(x + 1, DIMENSION_X), range(y - 1, -1, -1)):
            if BOARD[j][i] == '--':
                valid_moves.append((i, j))
            else:
                break
        # Check diagonally to the top-left
        for i, j in zip(range(x - 1, -1, -1), range(y - 1, -1, -1)):
            if BOARD[j][i] == '--':
                valid_moves.append((i, j))
            else:
                break

    elif piece == 'b_Kn' or piece == 'w_Kn':
        # Knight's L-shaped movement
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                        (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for dx, dy in knight_moves:
            new_x = x + dx
            new_y = y + dy

            if 0 <= new_x < DIMENSION_X and 0 <= new_y < DIMENSION_Y and BOARD[new_y][new_x] == '--':
                valid_moves.append((new_x, new_y))

    elif piece == 'b_P':
        # Black pawn moves downward
        if y + 1 < DIMENSION_Y and BOARD[y + 1][x] == '--':
            valid_moves.append((x, y + 1))
            if y == 1 and BOARD[y + 2][x] == '--':
                valid_moves.append((x, y + 2))

        # Capturing diagonally
        if y + 1 < DIMENSION_Y and x - 1 >= 0 and BOARD[y + 1][x - 1] != '--':
            valid_moves.append((x - 1, y + 1))
        if y + 1 < DIMENSION_Y and x + 1 < DIMENSION_X and BOARD[y + 1][x + 1] != '--':
            valid_moves.append((x + 1, y + 1))

    elif piece == 'w_P':
        # White pawn moves upward
        if y - 1 >= 0 and BOARD[y - 1][x] == '--':
            valid_moves.append((x, y - 1))
            if y == 4 and BOARD[y - 2][x] == '--':
                valid_moves.append((x, y - 2))

        # Capturing diagonally
        if y - 1 >= 0 and x - 1 >= 0 and BOARD[y - 1][x - 1] != '--':
            valid_moves.append((x - 1, y - 1))
        if y - 1 >= 0 and x + 1 < DIMENSION_X and BOARD[y - 1][x + 1] != '--':
            valid_moves.append((x + 1, y - 1))

    return valid_moves


## this should be deleted
def mark_valid_pos(WINDOW, VALID_POS):

    for position in VALID_POS:
        valid_rect = pygame.Rect(
            position[0] * SQ_SIZE, position[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(WINDOW, pygame.Color('red'), valid_rect, 3)


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

    # Get valid moves
    validMoves = GAME_STATE.getValidMoves()
    moveMade = False #flag variable when a move is made

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
                y_coord = event.pos[0] // SQ_SIZE
                x_coord = event.pos[1] // SQ_SIZE
                selectedSq.append((x_coord, y_coord))

                # mark selected piece
                SELECTED_PIECE = (y_coord, x_coord)
                pieceClickCount += 1

                # # check valid move
                # piece_id = GAME_STATE.board[x_coord][y_coord]
                # if piece_id != '--':
                #     valid_moves = get_valid_moves(
                #         piece_id, (y_coord, x_coord), GAME_STATE.board)
                #     valid_positions = valid_moves

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z: #undo when z is pressed
                    GAME_STATE.undoMove()
                    moveMade = True


        # update valid moves
        if moveMade:
            validMoves = GAME_STATE.getValidMoves()
            moveMade = False


        # Set Game State
        drawGameState(WINDOW, GAME_STATE, valid_positions)

        if pieceClickCount == 2:

            print(selectedSq[0], selectedSq[1])
            move = engine.Move(selectedSq[0], selectedSq[1], GAME_STATE.board)
            print(move.getChessNotation())
            
            # if move valid then make move
            if move in validMoves:
                GAME_STATE.makeMove(move)
                moveMade = True
            pieceClickCount = 0
            selectedSq = []

        # Draw red border if a piece is selected
        if SELECTED_PIECE is not None and pieceClickCount == 1:
            SELECTED_RECT = pygame.Rect(
                SELECTED_PIECE[0] * SQ_SIZE, SELECTED_PIECE[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(WINDOW, pygame.Color('blue'), SELECTED_RECT, 3)

        # Update the window state
        pygame.display.update()


if __name__ == '__main__':
    main()
