import random

class AI:
    def __init__(self):
        self.nextMove = None
        self.pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
        self.CHECKMATE = 100
        self.STALEMATE = 0
        self.DEPTH = 3
        
    
    # score the board based on material
    # black: trying to minimize score as possible
    # white: trying to maximize score as possible
    def scoreMaterial(self, gs):
        score = 0
        for row in gs.board:
            for square in row:
                if square[0] == "w":
                    score += self.pieceScore[square[1]]
                elif square[0] == "b":
                    score -= self.pieceScore[square[1]]
        return score

    def findRandomMove(self, validMoves):
        return validMoves[random.randint(0, len(validMoves) - 1)] 

