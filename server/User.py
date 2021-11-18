import json


class User:
    def __init__(self, userId, userName) -> None:
        self.uid = userId
        self.name = userName
        self.score = 0
    
    def getScore(self):
        return self.score
    
    def setScore(self, newScore):
        self.score = newScore

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)