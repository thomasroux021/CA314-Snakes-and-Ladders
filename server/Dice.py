import random

class Dice:
    def __init__(self) -> None:
        self.__value = 0
    
    def rollDice(self):
        self.__value = random.randint(1, 6)
        return self.__value
    
    def getCurrentValue(self):
        return self.__value