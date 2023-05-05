from AI.AI import AI

class Minimax(AI):
    # helper method to make first recursive call
    def findMove(self, gs, validMoves):
        self.findMoveMinimax(gs, validMoves, self.DEPTH, gs.whiteToMove)
        return self.nextMove

    def findMoveMinimax(self, gs, validMoves, depth, whiteToMove):
        if depth == 0:
            return self.scoreMaterial(gs)
        if whiteToMove: # try to maximize
            maxScore = -self.CHECKMATE
            for move in validMoves:
                gs.makeMove(move)
                nextMoves = gs.getAllValidMoves()
                score = self.findMoveMinimax(gs, nextMoves, depth-1, False)
                if score > maxScore:
                    maxScore = score
                    if depth == self.DEPTH:
                        self.nextMove = move
                gs.undoMove()
            return maxScore
        else: # try to minimize score
            minScore = self.CHECKMATE
            for move in validMoves:
                gs.makeMove(move)
                nextMoves = gs.getAllValidMoves()
                score = self.findMoveMinimax(gs, nextMoves, depth-1, True)
                if score < minScore:
                    minScore = score
                    if depth == self.DEPTH:
                        self.nextMove = move 
                gs.undoMove()
            return minScore

    # a positive socre is good for white 
    # a negative socre is good for black
    def scoreBoard(self, gs):
        if gs.checkMate:
            if gs.whiteToMove:
                return -self.CHECKMATE # black win
            else:
                return self.CHECKMATE # white win
        elif gs.staleMate:
            return self.STALEMATE
        score = 0
        for row in gs.board:
            for square in row:
                if square[0] == "w":
                    score += self.pieceScore[square[1]]
                elif square[0] == "b":
                    score -= self.pieceScore[square[1]]
        return score