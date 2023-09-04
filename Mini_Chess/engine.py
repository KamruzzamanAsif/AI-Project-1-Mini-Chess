class GameState():

    def __init__(self) -> None:

        self.board = [
            ['b_R', 'b_Kn', 'b_B', 'b_Q', 'b_K'],
            ['b_P', 'b_P', 'b_P', 'b_P', 'b_P'],
            ['--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--'],
            ['w_P', 'w_P', 'w_P', 'w_P', 'w_P'],
            ['w_R', 'w_Kn', 'w_B', 'w_Q', 'w_K'],
        ]

        self.whiteToMove = True
        self.moveLog = []

    #makes moves except castling, en passant, pawn promotion
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove


    ###>>>>>>>>>>>>   Move Generation Section <<<<<<<<<<<<<<<<<<

    # all moves with considering checks
    def getValidMoves(self):
        return self.getAllPossibleMoves()
    
    # all moves without considering checks
    def getAllPossibleMoves(self):
        moves = [Move((3,4), (4,4), self.board)]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)

        return moves 

    '''
    Get all the pawn moves for a pawn located at row, column and add these moves to list
    '''
    def getPawnMoves(self, r, c, moves):
        pass

    '''
    Get all the rook moves for a pawn located at row, column and add these moves to list
    '''
    def getRookMoves(self, r, c, moves):
        pass




class Move():

    ranksToRows = {
        "1": 5,
        "2": 4,
        "3": 3,
        "4": 2,
        "5": 1,
        "6": 0
    }
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4
    }
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board) -> None:

        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)
    
    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + ' >> ' + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
