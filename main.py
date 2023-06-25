import pygame as p
from AI.AI import AI 
from AI.Greedy import Greedy
from AI.Minimax import Minimax
from AI.Negamax import Negamax
from AI.Negascout import Negascout
from ChessEngine  import GameState, Move
from pygame import Color, Rect
from pygame.locals import *

WIDTH = HEIGHT = 512
DIMENSION = 8 # dimension of chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 20 # for animations
IMAGES = {}

AI = AI()
Greedy = Greedy()
Minimax = Minimax()
Negamax = Negamax()
Negascout = Negascout()


def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"img/{piece}.png"), (SQ_SIZE, SQ_SIZE))

# highlight square selected and moves for piece selected
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"): # sqSelected is a piece that can be moved  
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparent value, 0: transparent, 255: opaque 
            s.fill(p.Color("blue"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight moves from that square 
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

# responsible for all the graphics within a current game state
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) # draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) # draw pieces on top of those squares

# draw the squares on the board, top left square is always light
def drawBoard(screen):
    global colors
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

def animateMove(move, screen, board, clock):
    global colors
    coords = [] # list of coords that animation will be move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 # frames to move 1 square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square 
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece onto rectangle 
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))  
        p.display.flip()
        clock.tick(60)   

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 36, True, True)
    textObject = font.render(text, 0, p.Color("Blue"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    # textObject = font.render(text, 0, p.Color("Gray"))
    # screen.blit(textObject, textLocation.move(2, 2))

def main():
    p.init()
    p.display.set_caption("Hello World")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(Color("white"))
    gs = GameState()

    validMoves = gs.getAllValidMoves()
    moveMade = False
    animate = False # flag variable when animating a move

    loadImages()
    running = True
    sqSelected = () # no square is selected, keep track of the last click of user(tuple: (row, col))
    playerClicks = [] # keep track of player clicks (2 tuples: [(6, 4), (4, 4)])
    gameOver = False
    playerOne = True # if a human is playing white: true, if AI is playing white: false
    playerTwo = False # if a human is playing black: true, if AI is playing black: false

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE or e.key == K_q:
                    running = False

            # mouse handler 
            elif e.type == MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
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
                        # print(move.getChessNotation())
                        
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(move)
                                moveMade = True
                                animate = True
                                sqSelected = () # reset state
                                playerClicks = [] # reset state
                        if not moveMade:
                            playerClicks = [sqSelected]
                
            if e.type == KEYDOWN and e.key == K_z: # undo the last move
                print(1)
                gs.undoMove()
                validMoves = gs.getAllValidMoves()
                moveMade = True
                animate = False
                gameOver = False
            
            if e.type == KEYDOWN and e.key == K_r: # reset the board 
                gs = GameState()
                validMoves = gs.getAllValidMoves()
                sqSelected = ()
                playerClicks = []
                moveMade = False
                animate = False
                gameOver = False


            elif e.type == p.QUIT:
                running = False

        # AI move finder logic
        if not gameOver and not humanTurn:
            # AIMove = AI.findRandomMove(validMoves=validMoves)
            AIMove, maxScore, color = Greedy.findBestMove(gs=gs, validMoves=validMoves)
            # AIMove = Greedy.findBestMoveTwoLayer(gs=gs, validMoves=validMoves)
            # AIMove = Minimax.findMove(gs=gs, validMoves=validMoves)
            # AIMove = Negamax.findMove(gs=gs, validMoves=validMoves)
            # AIMove = Negascout.findMove(gs=gs, validMoves=validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getAllValidMoves()
            moveMade = False
            animate = False
        
        drawGameState(screen=screen, gs=gs, validMoves=validMoves, sqSelected=sqSelected)
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black is the winner")
            else:
                drawText(screen, "White is the winner")
        elif gs.staleMate:
            gameOver = True
            drawText(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip() # cap nhat lai man hinh


if __name__ == "__main__":
    main()

