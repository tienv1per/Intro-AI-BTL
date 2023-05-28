import pygame as p
import random
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
MAX_FPS = 15 # for animations
IMAGES = {}

def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"img/{piece}.png"), (SQ_SIZE, SQ_SIZE))

