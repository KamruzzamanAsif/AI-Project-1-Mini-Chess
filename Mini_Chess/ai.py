# initially we'll start from random moves
import random

pieceValue = {"K": 0, "Q": 10, "R": 3, "B": 3, "N": 5, "P": 3}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

# score the board based on material


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceValue[square[-1]]
            elif square[0] == 'b':
                score -= pieceValue[square[-1]]

    return score

# naive approach


def findBestMove(GAME_STATE, validMoves):
    if GAME_STATE.whiteToMove:
        turnMultiplier = 1
    else:
        turnMultiplier = -1

    maxScore = -CHECKMATE
    bestMove = None

    for playerMove in validMoves:
        GAME_STATE.makeMove(playerMove)

        if GAME_STATE.checkMate:
            score = CHECKMATE
        elif GAME_STATE.staleMate:
            score = STALEMATE
        else:
            score = turnMultiplier * scoreMaterial(GAME_STATE.board)
        if (score > maxScore):
            maxScore = score
            bestMove = playerMove

        GAME_STATE.undoMove()
    return bestMove
