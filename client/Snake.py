from Board import *
from Piece import *
from Container.Text import Text

class Snake:
    def __init__(self, start, end, displayGame, board, id = 0) -> None:
        self.posBottom = start
        self.posTop = end
        self.squareBottom = board.get_square(self.posBottom)
        self.squareTop = board.get_square(self.posTop)
        self.display_game = displayGame

        self.textIdBottom = Text(self.display_game, str(id) + "S", self.squareBottom.x + 30, self.squareBottom.y)
        self.textIdTop = Text(self.display_game, str(id) + "S", self.squareTop.x + 30, self.squareTop.y)
    
    def raisePiece(self, piece: Piece):
        piece.move(0, self.posBottom)
    
    def isOnSnakeHead(self, piece: Piece):
        return piece.position == self.posTop

    def draw(self):
        self.textIdBottom.draw()
        self.textIdTop.draw()
