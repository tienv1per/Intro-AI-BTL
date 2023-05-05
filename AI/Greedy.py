from AI.AI import AI

class Greedy(AI):
    def findBestMove(self, gs, validMoves):
        turnMultiplayer = 1 if gs.whiteToMove else -1 
        maxScore = -self.CHECKMATE
        bestMove = None
        for playerMove in validMoves:
            gs.makeMove(playerMove)
            score = turnMultiplayer * self.scoreMaterial(gs)
            gs.undoMove()
            if gs.checkMate:
                score = self.CHECKMATE
            elif gs.staleMate:
                score = self.STALEMATE
            else:
                maxScore = score
                bestMove = playerMove
        return bestMove 
