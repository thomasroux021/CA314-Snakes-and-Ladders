from math import atan, pi, sqrt, degrees, atan2
from Piece import Piece
from Square import Square
from Container.Text import Text
from Container.Image import Image

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
        
        distanceHyp = sqrt((self.squareTop.x - self.squareBottom.x)**2 + (self.squareTop.y - self.squareBottom.y)**2)
        angle = degrees(atan2(-1*(self.squareTop.y - self.squareBottom.y), self.squareTop.x - self.squareBottom.x))
        here = (min(self.squareBottom.x, self.squareTop.x), min(self.squareBottom.y, self.squareTop.y))
        path = "assets/ladder-medium.png"
        if (distanceHyp > 250):
            path = "assets/ladder-big.png"
        self.ladderImage = Image(self.display_game, path, self.squareTop.x, self.squareTop.y, 30, distanceHyp, angle, here)
    
    def raisePiece(self, piece: Piece):
        piece.move(0, self.posTop)
    
    def isOnLadderBottom(self, piece: Piece):
        return piece.position == self.posBottom

    def draw(self):
        # self.textIdBottom.draw()
        # self.textIdTop.draw()
        self.ladderImage.draw()
