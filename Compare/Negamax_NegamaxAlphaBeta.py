from AI_Eval.Negamax import Negamax

class Negamax_NegamaxAlphaBeta:
    def __init__(self):
        self.negamax = Negamax()
        self.turn = 0
    
    def findMove(self, gs, validMoves):
        next_move_negamax, total_node_negamax = self.negamax.findMove(gs, validMoves)
        next_move_negamax_pruning, total_node_negamax_pruning = self.negamax.findMoveAlphaBeta(gs, validMoves)
        self.turn += 1
        print("Turn: ", self.turn)
        print("negamax: ", total_node_negamax)
        print("negamax_pruning: ", total_node_negamax_pruning)
        print("-------------------------------------------------------\n")
        return next_move_negamax, self.turn, total_node_negamax, total_node_negamax_pruning         