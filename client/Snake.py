from math import sqrt, atan2, degrees
from Square import Square
from Piece import Piece
from Container.Text import Text
from Container.Image import Image

class Snake:
    def __init__(self, start, end, displayGame, board, id = 0) -> None:
        self.posTop = end
        self.posBottom = start
        self.squareBottom: Square = board.get_square(self.posBottom)
        self.squareTop: Square = board.get_square(self.posTop)
        self.display_game = displayGame

        self.textIdBottom = Text(self.display_game, str(id) + "S", self.squareBottom.x + 30, self.squareBottom.y)
        self.textIdTop = Text(self.display_game, str(id) + "S", self.squareTop.x + 30, self.squareTop.y)

        distanceHyp = sqrt((self.squareTop.x - self.squareBottom.x)**2 + (self.squareTop.y - self.squareBottom.y)**2)
        angle = degrees(atan2(-1*(self.squareTop.y - self.squareBottom.y), self.squareTop.x - self.squareBottom.x))
        here = (min(self.squareBottom.x, self.squareTop.x), min(self.squareBottom.y, self.squareTop.y))
        path = "assets/snake-little.png"
        if (distanceHyp > 200):
            path = "assets/snake-medium.png"
        if (distanceHyp > 350):
            path = "assets/snake-big.png"
        self.snakeImage = Image(self.display_game, path, self.squareTop.x, self.squareTop.y, 30, distanceHyp, angle, here)
    
    def raisePiece(self, piece: Piece):
        piece.move(0, self.posBottom)
    
    def isOnSnakeHead(self, piece: Piece):
        return piece.position == self.posTop

    def draw(self):
        # self.textIdBottom.draw()
        # self.textIdTop.draw()
        self.snakeImage.draw()
