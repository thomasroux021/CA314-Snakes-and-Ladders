from socket import SOCK_DGRAM
from time import sleep
from Server import *
from User import * 
from Piece import *
from Dice import *
from Utils import *

class Game:
    def __init__(self) -> None:
        self.players: List[User] = []
        self.pieces: List[Piece] = []
        self.dice = Dice()
        Server.getInstance().init()
        Server.getInstance().addListeningFct(self.event)
        Server.getInstance().listenEvent()
    
    def add_player(self, data, uuid):
        for player in self.players:
            if (player.uid == uuid):
                return
        self.players.append(User(uuid, data["name"]))
        print("Add player")
        
        Server.getInstance().sendToAll(Utils.all('UPDATE_PLAYER', {'players': json.dumps(self.players, default=lambda o: o.toJSON())}))
        return 0
    
    def add_piece(self, data, addr):
        for player in self.players:
            if (player.uid == addr):
                self.pieces.append(Piece(data["colour"], player))
                break
        Server.getInstance().sendToAll(Utils.all('UPDATE_PIECE', {'pieces': self.pieces}))
        return 0
    
    def start_game(self):
        Server.getInstance().sendToAll(Utils.all('START_GAME'))
    
    def roll_dice(self, data, addr):
        self.dice.rollDice()
        value = self.dice.getCurrentValue()
        Server.getInstance().sendToAll(Utils.all('SHOW_DICE_ROLL', {'value': value}))
        return value

    def event(self, data, addr, sock = None):
        switcher = {
            "ADD_PLAYER": self.add_player,
            "ADD_PIECE": self.add_piece,
            "ROLL_DICE": self.roll_dice
        }
        ret = switcher.get(data["type"], "default")(data["data"], addr)
        if (ret == 0 and sock != None):
            Server.getInstance().send({'event': data['type'], 'status':"Ok"}, sock)
        else:
            Server.getInstance().send({'status': 'Error', 'event': data["type"]})

Game()