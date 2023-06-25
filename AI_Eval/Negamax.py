import random

from AI.AI import AI

class Negamax(AI):
    def __init__(self):
        super().__init__()
        self.totalNodes = 0
    
    def findMove(self, gs, validMoves):
        self.totalNodes = 0
        random.shuffle(validMoves)
        self.findMoveNegaMax(gs, validMoves, self.DEPTH, 1 if gs.whiteToMove else -1)
        return self.nextMove, self.totalNodes

    def findMoveAlphaBeta(self, gs, validMoves):
        self.totalNodes = 0
        random.shuffle(validMoves)
        self.findMoveNegaMaxAlphaBeta(gs, validMoves, self.DEPTH, -self.CHECKMATE, self.CHECKMATE, 1 if gs.whiteToMove else -1)
        return self.nextMove, self.totalNodes

    def findMoveNegaMax(self, gs, validMoves, depth, turn):
        self.totalNodes += 1
        if depth == 0:
            return turn * self.scoreMaterial(gs)
        maxScore = -self.CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getAllValidMoves()
            score = -self.findMoveNegaMax(gs, nextMoves, depth-1, -turn)
            if score > maxScore:
                maxScore = score
                if depth == self.DEPTH:
                    self.nextMove = move
            gs.undoMove()
        return maxScore
    
    def findMoveNegaMaxAlphaBeta(self, gs, validMoves, depth, alpha, beta, turn): 
        self.totalNodes += 1
        if depth == 0:
            return turn * self.scoreMaterial(gs)
        maxScore = -self.CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getAllValidMoves()
            score = -self.findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turn)
            gs.undoMove()
            if score > maxScore:
                maxScore = score
                if depth == self.DEPTH:
                    self.nextMove = move
            if maxScore > alpha: # pruning happen
                alpha = maxScore # new best alpha
            if alpha >= beta:
                break
        return maxScore
    