import pygame
from AI.AI import AI
from AI.Greedy import Greedy
from AI.Minimax import Minimax
from AI.Negamax import Negamax
from AI.Negascout import Negascout
from ChessEngine import GameState, Move
from pygame import Color, Rect
from pygame.locals import *

import sys
import time


class ButtonNew:
    def __init__(self, text, width, height, pos, elevation, font, top_color='', bottom_color=''):
        # Core attributes
        self.pressed = False
        self.hovered = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color if top_color != '' else '#854d0e'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color if bottom_color != '' else '#334155'
        # text
        self.font = font
        self.text_surf = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen, self.bottom_color,
                         self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color,
                         self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)

    def check_click(self, mouse_pos, action=None, param=None):
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#ef4444'
            if self.hovered == False:
                self.hovered = True
                self.top_rect = self.top_rect.inflate(50, 10)
                self.bottom_rect = self.bottom_rect.inflate(50, 10)
            get_press = pygame.mouse.get_pressed()
            if get_press[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    if action != None:
                        if param != None:
                            action(param)
                        else:
                            action()
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#854d0e'
            if self.hovered == True:
                self.top_rect = self.top_rect.inflate(-50, -10)
                self.bottom_rect = self.bottom_rect.inflate(-50, -10)
            self.hovered = False


WIDTH = 720
HEIGHT = 720
DIMENSION = 8  # dimension of chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 20  # for animations
IMAGES = {}

AI = AI()
Greedy = Greedy()
Minimax = Minimax()
Negamax = Negamax()
Negascout = Negascout()

pygame.init()
algo_option = ['Greedy', 'Minimax', 'Negamax', 'Negascout']
chosen_algo = 'Greedy'
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")
new_cursor = pygame.image.load("assets/mouse.png")
new_cursor = pygame.transform.scale(new_cursor, size=(50, 50))
pygame.mouse.set_visible(False)
BG = pygame.image.load("assets/background.png")


def get_font(size):
    return pygame.font.Font("assets/SamuraiBlast.woff", size)


def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK",
              "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(
            pygame.image.load(f"img/{piece}.png"), (SQ_SIZE, SQ_SIZE))

# highlight square selected and moves for piece selected


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        # sqSelected is a piece that can be moved
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            # highlight selected square
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparent value, 0: transparent, 255: opaque
            s.fill(pygame.Color("blue"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight moves from that square
            s.fill(pygame.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

# responsible for all the graphics within a current game state


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)  # draw pieces on top of those squares

# draw the squares on the board, top left square is always light


def drawBoard(screen):
    global colors
    colors = [Color("white"), Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, Rect(
                c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# draw the pieces on the board using current gs.board


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":  # not empty space
                screen.blit(IMAGES[piece], Rect(
                    col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10  # frames to move 1 square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount,
                move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pygame.Rect(move.endCol*SQ_SIZE,
                                move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, endSquare)
        # draw captured piece onto rectangle
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], pygame.Rect(
            c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
        clock.tick(60)


def drawText(screen, text):
    font = pygame.font.SysFont("Helvitca", 36, True, True)
    textObject = font.render(text, 0, pygame.Color("Blue"))
    textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)


def play_game(screen, chosen_algo):
    pygame.display.set_caption("AI CHESS")
    pygame.mouse.set_visible(True)
    clock = pygame.time.Clock()
    gs = GameState()

    validMoves = gs.getAllValidMoves()
    moveMade = False
    animate = False  # flag variable when animating a move

    loadImages()
    running = True
    # no square is selected, keep track of the last click of user(tuple: (row, col))
    sqSelected = ()
    # keep track of player clicks (2 tuples: [(6, 4), (4, 4)])
    playerClicks = []
    gameOver = False
    playerOne = True  # if a human is playing white: true, if AI is playing white: false
    playerTwo = False  # if a human is playing black: true, if AI is playing black: false

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (
            not gs.whiteToMove and playerTwo)
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE or e.key == K_q:
                    print(123)
                    running = False

            # mouse handler
            elif e.type == MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = pygame.mouse.get_pos()  # (x, y): location of mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):  # user clicked same square twice
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
                                animate = True
                                sqSelected = ()  # reset state
                                playerClicks = []  # reset state
                        if not moveMade:
                            playerClicks = [sqSelected]

            if e.type == KEYDOWN and e.key == K_z:  # undo the last move
                gs.undoMove()
                validMoves = gs.getAllValidMoves()
                moveMade = True
                animate = False
                gameOver = False

            if e.type == KEYDOWN and e.key == K_r:  # reset the board
                gs = GameState()
                validMoves = gs.getAllValidMoves()
                sqSelected = ()
                playerClicks = []
                moveMade = False
                animate = False
                gameOver = False

            elif e.type == pygame.QUIT:
                running = False

        # AI move finder logic
        if not gameOver and not humanTurn:

            if chosen_algo == 'Greedy':
                AIMove = Greedy.findBestMove(gs=gs, validMoves=validMoves)
            elif chosen_algo == 'Minimax':
                AIMove = Minimax.findMove(gs=gs, validMoves=validMoves)
            elif chosen_algo == 'Negamax':
                AIMove = Negamax.findMove(gs=gs, validMoves=validMoves)
            elif chosen_algo == 'Negascout':
                AIMove = Negascout.findMove(gs=gs, validMoves=validMoves)

            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getAllValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen=screen, gs=gs,
                      validMoves=validMoves, sqSelected=sqSelected)
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
        pygame.display.flip()  # cap nhat lai man hinh


def play():
    while True:
        global chosen_algo
        SCREEN.blit(BG, (0, 0))
        play_game(SCREEN, chosen_algo)
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        pygame.display.update()


def choose_algo_action(algo):
    global chosen_algo
    chosen_algo = algo
    print(chosen_algo)
    play()


index = 0
options_list = []
for algo in algo_option:
    option_algo = ButtonNew(
        algo, 400, 80, (160, 160 + index), 5, get_font(30))
    index += 100
    options_list.append(option_algo)
OPTIONS_BACK = ButtonNew('BACK', 300, 80, (360 - 150, 600), 5, get_font(75))


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        global chosen_algo
        SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(55).render(
            "Choose algorithm", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(360, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK.draw(SCREEN)
        OPTIONS_BACK.check_click(OPTIONS_MOUSE_POS, main_menu)

        for i in range(len(options_list)):
            options_list[i].draw(SCREEN)
            options_list[i].check_click(
                OPTIONS_MOUSE_POS, choose_algo_action, algo_option[i])

        SCREEN.blit(new_cursor, OPTIONS_MOUSE_POS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

        pygame.display.update()


PLAY_BUTTON = ButtonNew('PLAY', 400, 100, (160, 250), 5, get_font(75))
QUIT_BUTTON = ButtonNew('QUIT', 400, 100, (160, 400), 5, get_font(75))


def main_menu():
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        MENU_TEXT = get_font(100).render("CHESS", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(360, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        PLAY_BUTTON.draw(SCREEN)
        PLAY_BUTTON.check_click(MENU_MOUSE_POS, options)
        QUIT_BUTTON.draw(SCREEN)
        QUIT_BUTTON.check_click(MENU_MOUSE_POS, exit_game)

        SCREEN.blit(new_cursor, MENU_MOUSE_POS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

        pygame.display.update()


def exit_game():
    pygame.quit()
    sys.exit()


main_menu()
