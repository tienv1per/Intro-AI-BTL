import random
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

    # find minimum of opponent's best move
    def findBestMoveTwoLayer(self, gs, validMoves):
        turnMultiplayer = 1 if gs.whiteToMove else -1
        opponentMinMaxScore = self.CHECKMATE
        bestPlayerMove = None
        random.shuffle(validMoves)
        for playerMove in validMoves:
            gs.makeMove(playerMove)
            opponentsMoves = gs.getAllValidMoves()
            if gs.staleMate:
                opponentMaxScore = self.STALEMATE
            elif gs.checkMate:
                opponentMaxScore = -self.CHECKMATE
            else:
                # try to maximize current score of opponent: maximize oppentMaxScore
                opponentMaxScore = -self.CHECKMATE
                for opponentMove in opponentsMoves:
                    gs.makeMove(opponentMove)
                    if gs.checkMate:
                        score = -turnMultiplayer * self.CHECKMATE
                    elif gs.staleMate:
                        score = self.STALEMATE
                    else:
                        score = -turnMultiplayer * self.scoreMaterial(gs)
                    if score > opponentMaxScore:
                        opponentMaxScore = score
                    gs.undoMove()
            # try to minimize next turn of opponent: try to minimize opponentMinMaxScore
            if opponentMaxScore < opponentMinMaxScore:
                opponentMinMaxScore = opponentMaxScore
                bestPlayerMove = playerMove
            gs.undoMove()
        return bestPlayerMove
