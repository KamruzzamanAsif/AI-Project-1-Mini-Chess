import sys

import pygame
from pygame.locals import *

import ai
import engine
import smartMove

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

def loadSoundEffects():

    effects = {}
    move_piece = pygame.mixer.Sound('./audios/move_pieces.wav')
    undo_move = pygame.mixer.Sound('./audios/undo_moves.wav')
    effects['move'] = move_piece
    effects['undo'] = undo_move
    return effects


def loadImages():

    IMAGES = {}
    pieces = ['b_B', 'b_K', 'b_N', 'b_P', 'b_Q', 'b_R',
              'w_B', 'w_K', 'w_N', 'w_P', 'w_Q', 'w_R']

    for piece in pieces:
        image = pygame.image.load('images/' + piece + '.png')
        IMAGES[piece] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))

    return IMAGES


'''
Highlight square selected
'''


def highlightSquare(WINDOW, GAME_STATE, validMoves, sqSelected, lastMove):

    if len(sqSelected) != 0:
        row, col = sqSelected[0]

        # a piece that can be moved
        if GAME_STATE.board[row][col][0] == ('w' if GAME_STATE.whiteToMove else 'b'):

            # hightlight square
            surface = pygame.Surface((SQ_SIZE, SQ_SIZE))
            # transparency value (0 - transparent, 255 - solid)
            surface.set_alpha(100)
            surface.fill(pygame.Color('blue'))
            WINDOW.blit(surface, (col*SQ_SIZE, row*SQ_SIZE))

            # highlight moves
            # TODO: if it's checkmate then the king should be colored as red

            surface.fill(pygame.Color('yellow'))

            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    WINDOW.blit(
                        surface, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

    # Highlight the last moved piece
    if len(lastMove) != 0:
        startRow, startCol = lastMove[0]
        endRow, endCol = lastMove[1]

        if startRow is not None and startCol is not None:
            surface = pygame.Surface((SQ_SIZE, SQ_SIZE))
            surface.set_alpha(100)
            surface.fill(pygame.Color('green'))
            WINDOW.blit(surface, (startCol*SQ_SIZE, startRow*SQ_SIZE))

        if endRow is not None and endCol is not None:
            surface = pygame.Surface((SQ_SIZE, SQ_SIZE))
            surface.set_alpha(100)
            surface.fill(pygame.Color('green'))
            WINDOW.blit(surface, (endCol*SQ_SIZE, endRow*SQ_SIZE))


def markMovedSquare(WINDOW, sqSelected):

    startRow, startCol = sqSelected[0]
    endRow, endCol = sqSelected[1]

    if startRow is not None and startCol is not None:
        print("ARE YOU THERE")
        surface = pygame.Surface((SQ_SIZE, SQ_SIZE))
        surface.set_alpha(100)
        surface.fill(pygame.Color('red'))
        WINDOW.blit(surface, (startCol*SQ_SIZE, startRow*SQ_SIZE))


def drawGameState(WINDOW, GAME_STATE, validMoves, sqSelected, lastMove):
    drawBoard(WINDOW)
    highlightSquare(WINDOW, GAME_STATE, validMoves, sqSelected, lastMove)
    drawPieces(WINDOW, GAME_STATE.board)
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


def drawPieces(WINDOW, Board):

    IMAGES = loadImages()

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


'''
Animating the piece movement
'''


def animateMove(move, WINDOW, board, clock):
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framePerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framePerSquare
    IMAGES = loadImages()

    for frame in range(frameCount + 1):
        row, col = (move.startRow + dR*frame/frameCount,
                    move.startCol + dC*frame/frameCount)

        # redraw the board
        drawBoard(WINDOW)
        drawPieces(WINDOW, board)

        # erase piece from ending square
        endSquare = pygame.Rect(move.endCol*SQ_SIZE,
                                move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(WINDOW, (BOARD_COLOR_A if (
            (move.endRow+move.endCol) % 2 == 0) else BOARD_COLOR_B), endSquare)

        # draw captured piece onto the square
        if move.pieceCaptured != '--':
            WINDOW.blit(IMAGES[move.pieceCaptured], endSquare)

        # draw moving piece
        WINDOW.blit(IMAGES[move.pieceMoved], pygame.Rect(
            col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.update()
        clock.tick(60)


########################## MAIN FUNCTION ##########################


def main():

    # initialize pygame
    pygame.init()

    # variables
    pieceClickCount = 0
    selectedSq = []
    animate = False
    # if human plays its TRUE, if AI plays then its FALSE (white)
    playerOne = True
    # -Do- (black)
    playerTwo = False
    lastMove = []

    # Set Display
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('♟️ Mini Chess ♟️')
    clock = pygame.time.Clock()

    # Set GameState
    GAME_STATE = engine.GameState()

    # Define the board area rect
    board_rect = pygame.Rect(
        0, 0, DIMENSION_X * SQ_SIZE, DIMENSION_Y * SQ_SIZE)

    # Button Rects
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

        # check if Human is playing...
        humanPlayer = (GAME_STATE.whiteToMove and playerOne) or (
            not GAME_STATE.whiteToMove and playerTwo)

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # Click squares to move the piece
                if board_rect.collidepoint(event.pos):
                    if humanPlayer:
                        y_coord = event.pos[0] // SQ_SIZE
                        x_coord = event.pos[1] // SQ_SIZE

                        # if same square is clicked twice then reset
                        if selectedSq == (x_coord, y_coord):
                            selectedSq = ()
                            pieceClickCount = 0
                        else:
                            selectedSq.append((x_coord, y_coord))
                            pieceClickCount += 1

                        # when the piece are to be moved
                        if pieceClickCount == 2:

                            move = engine.Move(
                                selectedSq[0], selectedSq[1], GAME_STATE.board)
                            print(move.getChessNotation())

                            # if move is valid then make move
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    GAME_STATE.makeMove(move)
                                    moveMade = True
                                    animate = True
                                    lastMove = selectedSq

                                    # playing move piece sound
                                    sound_effects = loadSoundEffects()
                                    sound_effects['move'].play()

                                    pieceClickCount = 0
                                    selectedSq = []

                            if not moveMade:
                                pieceClickCount = 1
                                selectedSq.remove(selectedSq[0])

                # Check if "Play" button is clicked
                if play_button_rect.collidepoint(event.pos):
                    print("Play button pressed")

                # Check if "Restart" button is clicked
                if restart_button_rect.collidepoint(event.pos):
                    GAME_STATE = engine.GameState()
                    validMoves = GAME_STATE.getValidMoves()
                    selectedSq = []
                    pieceClickCount = 0
                    moveMade = False
                    animate = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:  # undo when z is pressed
                    GAME_STATE.undoMove()
                    moveMade = True
                    animate = False

        # update valid moves
        if moveMade:
            if animate:
                animateMove(GAME_STATE.moveLog[-1],
                            WINDOW, GAME_STATE.board, clock)
            validMoves = GAME_STATE.getValidMoves()
            moveMade = False
            animate = False

        #! AI Move
        if not humanPlayer:
            # aiMove = ai.findRandomMove(validMoves)          # random ai move
            # aiMove = ai.findBestMove(GAME_STATE, validMoves)  # naive approach

            aiMove = smartMove.findBestMove(
                GAME_STATE, validMoves)  # optimum approach
            GAME_STATE.makeMove(aiMove)
            moveMade = True
            animate = True

            # playing piece moving sound
            sound_effects = loadSoundEffects()
            sound_effects['move'].play()

            # track last move
            lastMove = [(aiMove.startRow, aiMove.startCol),
                        (aiMove.endRow, aiMove.endCol)]

        # Set Game State
        drawGameState(WINDOW, GAME_STATE, validMoves, selectedSq, lastMove)

        # Update the window state
        pygame.display.update()


if __name__ == '__main__':
    main()
