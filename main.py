# handle user input and display 
import pygame as p
from Engine  import GameState, Move
from pygame import Color, Rect
from pygame.locals import *

WIDTH = HEIGHT = 512
DIMENSION = 8 # dimension of chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animations
IMAGES = {}


def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"img/{piece}.png"), (SQ_SIZE, SQ_SIZE))

# responsible for all the graphics within a current game state
def drawGameState(screen, gs):
    drawBoard(screen) # draw squares on the board
    drawPieces(screen, gs.board) # draw pieces on top of those squares

# draw the squares on the board, top left square is always light
def drawBoard(screen):
    colors = [Color("white"), Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
# draw the pieces on the board using current gs.board
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--": # not empty space
                screen.blit(IMAGES[piece], Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

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
    sqSelected = () # no square is selected, keep track of the last click of user(tuple: (row, col))
    playerClicks = [] # keep track of player clicks (2 tuples: [(6, 4), (4, 4)])

    while running:
        for e in p.event.get():
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE or e.key == K_q:
                    running = False

            elif e.type == MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y): location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col): # user clicked same square twice
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True

                    sqSelected = () # reset state
                    playerClicks = [] #reset state
                
            if e.type == KEYDOWN and e.key == K_z:
                gs.undoMove()
                validMoves = gs.getAllValidMoves()

            elif e.type == p.QUIT:
                running = False

        if moveMade:
            validMoves = gs.getAllValidMoves()

        drawGameState(screen=screen, gs=gs)
        clock.tick(MAX_FPS)
        p.display.flip() # cap nhat lai man hinh


if __name__ == "__main__":
    main()

