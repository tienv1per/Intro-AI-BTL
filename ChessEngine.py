# store all information about current state of chess game
# responsible for determining valid moves at current state
# keep move log

class GameState():
    def __init__(self) -> None:
        # board is 8x8 2D list, each element of the list has 2 characters
        # 1st char represent color of pieces: "b" or "w"
        # 2nd char represent tyoe of pieces: "K", "Q", "R", "B", "N", "P"
        # "--" represent em[ty space that currently contain no pieces.]
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.makefunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves, 
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove # swap players
        # update king's location
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
        
        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"

    
    # undo the last move made
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            
            self.staleMate = False
            self.checkMate = False
    
    # get all the moves with checkmate
    def getAllValidMoves(self):
        # generate all possible moves 
        moves = self.getAllPossibleMoves()
        # for each move, make the move 
        # for i in range(len(moves) - 1, -1, -1):
        for i  in range(len(moves) -1, -1, -1):
            self.makeMove(moves[i])
            # generate all opponent's moves 
            # for each of your opponent's moves, see if they attack yur king 
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                # if they attack king, not a valid move
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else: 
                self.staleMate = True
        return moves
    
    # check if the king is currently checked
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else: 
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])        
    
    # check if the location (r, c) can be attacked by opponent
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # switch to opponent's turn
        rivalMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in rivalMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    # get all possible moves without checkmate
    def getAllPossibleMoves(self):
        moves = [] # check if move we mousedown with the move we defined here
        for r in range(len(self.board)): # number of rows
            for c in range(len(self.board[r])): # number of cols in given row
                turn = self.board[r][c][0] # color of chess
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.makefunctions[piece](r, c, moves)        
        return moves

    # get all possible moves for pawn and add this move to the list moves
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: 
            if r -1 >= 0:
                if self.board[r-1][c] == "--": # tien len 1 buoc
                    moves.append(Move((r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--": # nuoc di dau, tien 2 buoc
                        moves.append(Move((r, c), (r-2, c), self.board))
                
                if c - 1 >= 0: # capture to the left
                    if self.board[r-1][c-1][0] == "b": # kiem tra quan den
                        moves.append(Move((r, c), (r-1, c-1), self.board))
                if c + 1 <= 7: # capture to the right
                    if self.board[r-1][c+1][0] == "b":
                        moves.append(Move((r, c), (r-1, c+1), self.board))

        else: # black pawn moves
            if r + 1 <= 7:
                if self.board[r+1][c] == "--":
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move((r, c), (r+2, c), self.board))
                
                if c - 1 >= 0:
                    if self.board[r+1][c-1][0] == "w":
                        moves.append(Move((r, c), (r+1, c-1), self.board))
                if c + 1 <= 7:
                    if self.board[r+1][c+1][0] == "w":
                        moves.append(Move((r, c), (r+1, c+1), self.board))

    # get all possible moves for rook and add this move to the list moves
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"
        
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break # an quan doi phuong, ko the di tiep
                    else: # quan dong minh
                        break
                else: 
                    break
    
    def getKnightMoves(self, r, c, moves):
        directions = ((-2, 1), (-2, -1), (-1, 2), (-1, -2),
                      (1, -2), (2, -1), (1, 2), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"

        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # doi phuong hoac o trong
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break # an quan doi phuong, ko the di tiep
                    else: # quan dong minh
                        break
                else: 
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves) 

    def getKingMoves(self, r, c, moves):
        directions = ((-1, 0), (-1, 1), (0, 1), (1, 1), 
                      (1, 0), (1, -1), (0, -1), (-1, -1))
        allyColor = "w" if self.whiteToMove else "b"

        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    
class Move():
    rankToRows = {
        "1": 7, "2": 6, "3": 5, "4": 4,
        "5": 3, "6": 2, "7": 1, "8": 0
    }

    rowToRanks = {v: k for k, v in rankToRows.items()}

    filesToCols = {
        "a": 0, "b": 1, "c": 2, "d": 3,
        "e": 4, "f": 5, "g": 6, "h": 7
    }

    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol] # gia tri quan co duoc move
        self.pieceCaptured = board[self.endRow][self.endCol] # gia tri quan co (hoac o trong) bi thay the
        # pawn promotion
        self.isPawnPromotion = False
        self.promotionChoice = "Q"
        if (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7):
            self.isPawnPromotion = True
        
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    # override equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return other.moveID == self.moveID


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowToRanks[r]