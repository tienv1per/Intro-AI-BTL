import pygame as p
from Compare.Minimax_Negamax import Minimax_Negamax
from Compare.Negamax_NegamaxAlphaBeta import Negamax_NegamaxAlphaBeta
from Compare.NegamaxAlphaBeta_Negascout import NegamaxAlphaBeta_Negascout
from ChessEngine  import GameState, Move
from pygame import Color, Rect
from pygame.locals import *

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 20
IMAGES = {}

Minimax_Negamax = Minimax_Negamax()
Negamax_NegamaxAlphaBeta = Negamax_NegamaxAlphaBeta()
NegamaxAlphaBeta_Negascout = NegamaxAlphaBeta_Negascout()


def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"img/{piece}.png"), (SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) 
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) 

def drawBoard(screen):
    global colors
    colors = [Color("white"), Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def writeLog(filename, content):
    try:
        with open(filename, "a") as f:
            f.write(content)
    except IOError:
        print("An error occurred while writing to the file.")


def main():
    p.init()
    p.display.set_caption("Hello World")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(Color("white"))
    gs = GameState()

    validMoves = gs.getAllValidMoves()
    moveMade = False

    loadImages()
    running = True
    sqSelected = () 
    playerClicks = [] 
    gameOver = False
    playerOne = True 
    playerTwo = False 

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE or e.key == K_q:
                    running = False

            elif e.type == MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() 
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col): 
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                    if len(playerClicks) == 2:
                        move = Move(playerClicks[0], playerClicks[1], gs.board)
                        
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(move)
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
                
            if e.type == KEYDOWN and e.key == K_z: 
                gs.undoMove()
                validMoves = gs.getAllValidMoves()
                moveMade = True
                gameOver = False
            
            if e.type == KEYDOWN and e.key == K_r: 
                gs = GameState()
                validMoves = gs.getAllValidMoves()
                sqSelected = ()
                playerClicks = []
                moveMade = False
                gameOver = False


            elif e.type == p.QUIT:
                running = False

        if not gameOver and not humanTurn:
            AIMove, turn, total_1, total_2 = Minimax_Negamax.findMove(gs, validMoves)
            # AIMove, turn, total_1, total_2 = Negamax_NegamaxAlphaBeta.findMove(gs, validMoves)
            # AIMove, turn, total_1, total_2 = NegamaxAlphaBeta_Negascout.findMove(gs, validMoves)
            filename = "Minimax_Negamax.txt"
            content = "Turn: {}\nminimax: {}\nnegamax: {}\n-------------------------------------------------------\n".format(turn, total_1, total_2)
            writeLog(filename, content)
            gs.makeMove(AIMove)
            moveMade = True

        if moveMade:
            validMoves = gs.getAllValidMoves()
            moveMade = False
        
        drawGameState(screen=screen, gs=gs, validMoves=validMoves, sqSelected=sqSelected)
        if gs.checkMate or gs.staleMate:
            gameOver = True

        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()

