from AI_Eval.Minimax import Minimax
from AI_Eval.Negamax import Negamax

class Minimax_Negamax:
    def __init__(self):
        self.minimax = Minimax()
        self.negamax = Negamax()
        self.turn = 0
    
    def findMove(self, gs, validMoves):
        next_move_minimax, total_node_minimax = self.minimax.findMove(gs, validMoves)
        next_move_negamax, total_node_negamax = self.negamax.findMove(gs, validMoves)
        self.turn += 1
        print("Turn: ", self.turn)
        print("minimax: ", total_node_minimax)
        print("negamax: ", total_node_negamax)
        print("-------------------------------------------------------\n")
        return next_move_negamax, self.turn, total_node_minimax, total_node_negamax         