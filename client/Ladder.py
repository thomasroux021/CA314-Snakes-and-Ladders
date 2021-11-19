from Piece import Piece
from Square import Square

class Ladder:
    def __init__(self, start, end, displayGame, board) -> None:
        self.posBottom = start
        self.posTop = end
        self.squareBottom: Square = board.get_square(self.posBottom)
        self.squareTop: Square = board.get_square(self.posTop)
        self.display_game = displayGame
    
    def raisePiece(self, piece: Piece):
        piece.move(0, self.posTop)
    
    def isOnLadderBottom(self, piece: Piece):
        return piece.position == self.posBottom

    def draw():
        return
