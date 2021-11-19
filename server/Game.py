from socket import SOCK_DGRAM
from time import sleep
import random
from Board import *
from Server import *
from Color import *
from User import * 
from Piece import *
from Dice import *
from Utils import *

class Game:
    def __init__(self) -> None:
        self.colors = self.init_color()
        self.players: List[User] = []
        self.dice = Dice()
        self.game_start = False
        self.player_turn = None
        self.board = None
        Server.getInstance().init(self.remove_player)
        Server.getInstance().addListeningFct(self.event)
        Server.getInstance().listenEvent()

    def init_color(self):
        colors = [Color.aqua, Color.pink, Color.purple, Color.green]
        random.shuffle(colors)
        return colors

    def remove_player(self, data, uid):
        for i, player in enumerate(self.players):
            if (player.uid == uid):
                self.colors.append(player.color)
                random.shuffle(self.colors)
                self.players.pop(i)
        if (len(self.players) == 0):
            self.end_game()
        elif (self.player_turn and self.player_turn.uid == uid):
            self.player_turn = self.players.pop(0)
            self.players.append(self.player_turn)
            Server.getInstance().sendToAll(Utils.all('PLAYER_TURN', {'uid': self.player_turn.uid}))
            Server.getInstance().sendToAll(Utils.all('UPDATE_PLAYERS', 
                {'players': [{
                    'uid': player.uid,
                    'username': player.username,
                    'color': player.color
                } for player in self.players]
            }))
    
    def add_player(self, data, uid):
        if (self.game_start):
            return
        for player in self.players:
            if (player.uid == uid):
                return
        self.players.append(User(uid, data["username"], self.colors.pop()))
        print("Add player")
        
        Server.getInstance().sendToAll(Utils.all('LIST_PLAYERS', 
            {'players': [{
                'uid': player.uid,
                'username': player.username,
                'color': player.color
            } for player in self.players]
        }))
        if (len(self.players) == 4):
            self.start_game()
    
    def start_game(self):
        self.game_start = True
        self.board = Board(random.randint(4,8), random.randint(4,8))
        random.shuffle(self.players)
        Server.getInstance().sendToAll(Utils.all('GAME_START', {
            'snakes': [snake for snake in self.board.snakes],
            'ladders': [ladder for ladder in self.board.ladders],
            'order': [player.uid for player in self.players]
        }))
        self.player_turn = self.players.pop(0)
        self.players.append(self.player_turn)
        Server.getInstance().sendToAll(Utils.all('PLAYER_TURN', {'uid': self.player_turn.uid}))
    
    def end_game(self):
        if (self.player_turn):
            Server.getInstance().sendToAll(Utils.all('GAME_END', {'uid': self.player_turn.uid}))
        self.colors = self.init_color()
        self.players = []
        self.player_turn = None
        self.board = None
        self.game_start = False

    def roll_dice(self, data, addr):
        if (addr != self.player_turn.uid):
            return
        Server.getInstance().sendToAll(Utils.all('PLAYER_ROLLING_DICE', {}))
        time.sleep(2)
        self.dice.rollDice()
        value = self.dice.getCurrentValue()
        self.player_turn.updatePosition(self.board, value)
        Server.getInstance().sendToAll(Utils.all('PLAYER_DICE', {
            'value': value,
            'uid': addr,
            'position': self.player_turn.position
        }))
        if (self.player_turn.position == self.board.square):
            self.end_game()
        else:
            if (value != 6):
                self.player_turn = self.players.pop(0)
                self.players.append(self.player_turn)
            Server.getInstance().sendToAll(Utils.all('PLAYER_TURN', {'uid': self.player_turn.uid}))

    def event(self, data, addr, sock = None):
        switcher = {
            "ADD_PLAYER": self.add_player,
            "REMOVE_PLAYER": self.remove_player,
            "ROLL_DICE": self.roll_dice,
        }
        switcher.get(data["event"], "default")(data["data"], addr)

Game()