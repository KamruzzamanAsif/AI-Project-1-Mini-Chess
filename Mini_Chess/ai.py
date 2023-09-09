import random

pieceValue = {"K": 100, "Q": 10, "R": 4, "B": 4, "N": 7, "P": 1}
CHECKMATE = float('inf')
STALEMATE = 0
DEPTH = 4


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gamestate, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    MinMaxWithPruning(gamestate, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gamestate.whiteToMove else -1)
    return nextMove

def MinMaxWithPruning(gamestate, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gamestate)

    maxScore = -CHECKMATE
    for move in validMoves:
        gamestate.makeMove(move)
        nextMoves = gamestate.getValidMoves()
        score = -MinMaxWithPruning(gamestate, nextMoves,
                                        depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move

        gamestate.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:       # pruning
            break

    return maxScore

# positive is good for white and negative is good for black


def scoreBoard(gamestate):
    if gamestate.checkMate:
        if gamestate.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE

    elif gamestate.staleMate:
        return STALEMATE

    score = 0
    for row in gamestate.board:
        for square in row:
            if square[0] == 'w':
                score += pieceValue[square[-1]]
            elif square[0] == 'b':
                score -= pieceValue[square[-1]]

    return score
