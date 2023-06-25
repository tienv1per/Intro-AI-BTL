from AI_Eval.Negamax import Negamax
from AI_Eval.Negascout import Negascout

class NegamaxAlphaBeta_Negascout:
    def __init__(self):
        self.negamax = Negamax()
        self.negascout = Negascout()
        self.turn = 0
    
    def findMove(self, gs, validMoves):
        next_move_negascout, total_node_negascout = self.negascout.findMove(gs, validMoves)
        next_move_negamax_pruning, total_node_negamax_pruning = self.negamax.findMoveAlphaBeta(gs, validMoves)
        self.turn += 1
        print("Turn: ", self.turn)
        print("negamax_pruning: ", total_node_negamax_pruning)
        print("negascout: ", total_node_negascout)
        print("-------------------------------------------------------\n")
        return next_move_negascout, self.turn, total_node_negamax_pruning, total_node_negascout         