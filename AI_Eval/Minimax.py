import random
from AI.AI import AI

class Minimax(AI):
    def __init__(self):
        super().__init__()
        self.totalNodes = 0    

    # helper method to make first recursive call
    def findMove(self, gs, validMoves):
        self.totalNodes = 0
        random.shuffle(validMoves)
        self.findMoveMinimax(gs, validMoves, self.DEPTH, gs.whiteToMove)
        alpha = -self.CHECKMATE
        beta = self.CHECKMATE
        return self.nextMove, self.totalNodes

    def findMoveMinimax(self, gs, validMoves, depth, whiteToMove):
        self.totalNodes += 1
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