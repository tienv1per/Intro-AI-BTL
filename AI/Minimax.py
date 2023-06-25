import random
from AI.AI import AI

class Minimax(AI):
    # helper method to make first recursive call
    def findMove(self, gs, validMoves):
        self.counter = 0
        self.turn += 1
        random.shuffle(validMoves)
        alpha = -self.CHECKMATE
        beta = self.CHECKMATE
        bestScore = self.findMoveMiniMaxAlphaBeta(gs, validMoves, self.DEPTH, alpha, beta, True)
        print(f"Turn: {self.turn}, bestScore: {bestScore}, movesNum: {self.counter}, move: {self.nextMove.getChessNotation()}")
        return self.nextMove

    def findMoveMinimax(self, gs, validMoves, depth, whiteToMove):
        self.counter += 1
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
    
    def findMoveMiniMaxAlphaBeta(self, gs, validMoves, depth, alpha, beta, whiteToMove):
        if depth == 0:
            return self.scoreBoard(gs)
        if whiteToMove:
            maxScore = -self.CHECKMATE
            for move in validMoves:
                gs.makeMove(move)
                nextMoves = gs.getAllValidMoves()
                score = self.findMoveMiniMaxAlphaBeta(gs, nextMoves, depth-1, alpha, beta, False)
                gs.undoMove()
                if score > maxScore:
                    maxScore = score
                    if depth == self.DEPTH:
                        self.nextMove = move
                alpha = max(alpha, maxScore)
                if alpha >= beta:
                    break
            return maxScore
        else:
            minScore = self.CHECKMATE
            for move in validMoves:
                gs.makeMove(move)
                nextMoves = gs.getAllValidMoves()
                score = self.findMoveMiniMaxAlphaBeta(gs, nextMoves, depth-1, alpha, beta, True)
                gs.undoMove()
                if score < minScore:
                    minScore = score
                    if depth == self.DEPTH:
                        self.nextMove = move
                beta = min(beta, minScore)
                if alpha >= beta:
                    break
            return minScore