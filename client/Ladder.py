from Piece import Piece
from Square import Square
from Container.Text import Text

class Ladder:
    def __init__(self, start, end, displayGame, board, id = 0) -> None:
        self.posBottom = start
        self.posTop = end
        self.squareBottom: Square = board.get_square(self.posBottom)
        self.squareTop: Square = board.get_square(self.posTop)
        self.display_game = displayGame
        self.id = id

        self.textIdBottom = Text(self.display_game, str(id) + "L", self.squareBottom.x + 30, self.squareBottom.y)
        self.textIdTop = Text(self.display_game, str(id) + "L", self.squareTop.x + 30, self.squareTop.y)
    
    def raisePiece(self, piece: Piece):
        piece.move(0, self.posTop)
    
    def isOnLadderBottom(self, piece: Piece):
        return piece.position == self.posBottom

    def draw(self):
        self.textIdBottom.draw()
        self.textIdTop.draw()
