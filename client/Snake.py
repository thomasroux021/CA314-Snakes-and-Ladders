from Board import *
from Piece import *

class Snake:
    def __init__(self, start, end, displayGame, board) -> None:
        self.posBottom = start
        self.posTop = end
        self.squareBottom = board.get_square(self.posBottom)
        self.squareTop = board.get_square(self.posTop)
        self.display_game = displayGame
    
    def raisePiece(self, piece: Piece):
        piece.move(0, self.posBottom)
    
    def isOnSnakeHead(self, piece: Piece):
        return piece.position == self.posTop

    def draw():
        return
