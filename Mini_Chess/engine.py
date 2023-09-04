class GameState():

    def __init__(self) -> None:

        self.board = [
            ['b_R', 'b_N', 'b_B', 'b_Q', 'b_K'],
            ['b_P', 'b_P', 'b_P', 'b_P', 'b_P'],
            ['--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--'],
            ['w_P', 'w_P', 'w_P', 'w_P', 'w_P'],
            ['w_R', 'w_N', 'w_B', 'w_Q', 'w_K'],
        ]

        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves,
                              'N': self.getKnightMoves, 'B': self.getBishopMoves,
                              'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []

    # makes moves except castling, en passant, pawn promotion
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self, mode='single'):
        if mode == 'all':
            while len(self.moveLog) != 0:
                move = self.moveLog.pop()
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = move.pieceCaptured
                self.whiteToMove = not self.whiteToMove

        elif len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    # >>>>>>>>>>>>   Move Generation Section <<<<<<<<<<<<<<<<<<

    # all moves with considering checks

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    # all moves without considering checks
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][2]
                    self.moveFunctions[piece](r, c, moves) # calls the appropriate move function based on piece
        return moves



    '''
    Get all the pawn moves for a pawn located at row, column and add these moves to list
    '''

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # white pawn moves
            if r > 0: # row index checking
                if self.board[r-1][c] == "--": # 1 square pawn advance
                    moves.append(Move((r,c), (r-1, c), self.board))
                if c-1 > -1:
                    if self.board[r-1][c-1][0] == 'b': # left corner enemy piece to capture
                        moves.append(Move((r,c), (r-1, c-1), self.board))
                if c+1 < 5:
                    if self.board[r-1][c+1][0] == 'b': # right corner enemy piece to capture
                        moves.append(Move((r,c), (r-1, c+1), self.board))

        else: # black pawn moves
            if r < 5: # row index checking
                if self.board[r+1][c] == "--": # 1 square pawn advance
                    moves.append(Move((r,c), (r+1, c), self.board))
                if c-1 > -1:
                    if self.board[r+1][c-1][0] == 'w': # right corner enemy piece to capture
                        moves.append(Move((r,c), (r+1, c-1), self.board))
                if c+1 < 5:
                    if self.board[r+1][c+1][0] == 'w': # left corner enemy piece to capture
                        moves.append(Move((r,c), (r+1, c+1), self.board))
                    
        
    '''
    Get all the rook moves for a rook located at row, column and add these moves to list
    '''

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # up, left, down right
        enemyColor = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for i in range(1, 6):
                endRow = r + d[0]*i
                endCol = c + d[1]*i

                if 0<= endRow < 6 and 0<= endCol < 5:   # check on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--': # empty space so valid
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else: # friendly piece (own piece)
                        break
                else: # off board
                    break 

                        


    '''
    Get all the knight moves for a knight located at row, column and add these moves to list
    '''

    def getKnightMoves(self, r, c, moves):
        pass


    '''
    Get all the bishop moves for a bishop located at row, column and add these moves to list
    '''

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # all 4 diagonals
        enemyColor = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for i in range(1, 5): # a bishop can move maximum 4 diagonal squares
                endRow = r + d[0]*i
                endCol = c + d[1]*i

                if 0<= endRow < 6 and 0<= endCol < 5:   # check on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--': # empty space so valid
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else: # friendly piece (own piece)
                        break
                else: # off board
                    break 


    '''
    Get all the queen moves for a queen located at row, column and add these moves to list
    '''

    def getQueenMoves(self, r, c, moves):
        pass


    '''
    Get all the king moves for a king located at row, column and add these moves to list
    '''

    def getKingMoves(self, r, c, moves):
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
        self.moveID = self.startRow * 1000 + self.startCol * \
            100 + self.endRow * 10 + self.endCol
        # print(self.moveID)

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
