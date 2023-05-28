import random 
from AI.AI import AI

class Negascout(AI):
    def findMove(self, gs, validMoves):
        random.shuffle(validMoves)
        self.counter = 0
        self.findMoveNegascout(gs, validMoves, self.DEPTH, -self.CHECKMATE, self.CHECKMATE, 1 if gs.whiteToMove else -1)
        return self.nextMove

    def findMoveNegascout(self, gs, validMoves, depth, alpha, beta, turn):
        self.counter += 1
        bestMove = None
        if depth == 0:
            return turn * self.scoreMaterial(gs)
        for i, move in enumerate(validMoves):
            gs.makeMove(move)
            nextMoves = gs.getAllValidMoves()
            if i == 0:
                score = -self.findMoveNegascout(gs, nextMoves, depth-1, -beta, -alpha, -turn)
            else:
                score = -self.findMoveNegascout(gs, nextMoves, depth-1, -alpha-1, -alpha, -turn)
                if alpha < score < beta:
                    score = -self.findMoveNegascout(gs, nextMoves, depth-1, -beta, -score, -turn)
            gs.undoMove()
            if alpha < score:
                bestMove = move
                alpha = score
            if alpha >= beta:
                break
        if depth == self.DEPTH:
            self.nextMove = bestMove
        return alpha