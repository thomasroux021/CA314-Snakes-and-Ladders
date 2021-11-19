import json
from Board import *

class User:
    def __init__(self, userId, userName, color) -> None:
        self.uid = userId
        self.username = userName
        self.color = color
        self.position = 0
        self.score = 0
    
    def getScore(self):
        return self.score
    
    def setScore(self, newScore):
        self.score = newScore

    def update(self, username, color):
        self.username = username
        self.color = color

    def updatePosition(self, board, val):
        position = self.position + val
        for start, end in board.snakes:
            if (position == start):
                position = end
        for start, end in board.ladders:
            if (position == start):
                position = end
        self.position = max(board.square, position)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)