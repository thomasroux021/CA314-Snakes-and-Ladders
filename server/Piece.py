import json


class Piece:
    def __init__(self, userColour, user):
        self.colour = userColour
        self.user = user
        self.currentSquare = 1
    
    def movePiece(self, diceValue):
        self.currentSquare += diceValue
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)