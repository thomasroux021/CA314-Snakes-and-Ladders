from typing import List
from pygame import *
import os
from Client import *
from dotenv import load_dotenv

from Board import *
from Constant import *
from Piece import *
from Player import *
from Dice import *
from Snake import Snake
from Ladder import Ladder
from Menu import *

from Utils import Utils

load_dotenv()

class Game():
    def __init__(self) -> None:
        Client.getInstance().init(self.event)
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.uid = None
        self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption('Snakes And Ladders')
        pygame.font.init()

        self.gameView = [True, False, False, False]
        self.gameRun = True
        self.myTurn = False

        self.clock = pygame.time.Clock()
        self.dice = Dice(self.gameDisplay)
        self.board = Board(self.gameDisplay)
        self.menu = Menu(self.gameDisplay, self.quit_game, self.join_queue)

        self.playerWinner = None

        self.players: List[Player] = []
        self.snakes: List[Snake] = []
        self.ladders: List[Ladder] = []
        self.draw()


    def draw(self):
        try:
            while self.gameRun:
                self.gameDisplay.fill(Constant.back)
                Client.getInstance().receive()
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        self.gameRun = False
                    if (self.gameView[Constant.MENU]):
                        self.menu.handle_event(event)
                if (self.gameView[Constant.MENU]):
                    self.menu.draw()
                else:
                    self.board.draw()
                    self.dice.draw()
                pygame.display.update()
                self.clock.tick(60)
            pygame.quit()
        except KeyboardInterrupt:
            pygame.quit()
            sys.exit()

    def quit_game(self):
        self.gameRun = False

    def join_queue(self):
        Client.getInstance().send(Utils.all("ADD_PLAYER", {'username': self.menu.get_username(), 'uid': self.uid}))
        self.gameView[Constant.MENU] = False
        self.gameView[Constant.MATCH_MAKING] = True

    def me(self, data):
        self.uid = data['uid']
        # Client.getInstance().send(Utils.all("ADD_PLAYER", {'username': 'Remi', 'uid': self.uid}))
    
    def list_player(self, data):
        for dataPlayer in data["players"]:
            player = list(filter(lambda x: x.uid == dataPlayer["uid"], self.players))
            if (not player):
                newPiece = Piece.Piece(self.gameDisplay, dataPlayer["color"], self.board, dataPlayer["uid"])
                self.players.append(Player(dataPlayer["uid"], dataPlayer["username"], newPiece))
                self.gameView[Constant.MENU] = False
                self.gameView[Constant.MATCH_MAKING] = True
            else:
                continue
    
    def game_start(self, data):
        self.board.event_add_snakes_ladders(data["snakes"], data["ladders"])
        odered_list_player = []
        for uid in data["order"]:
            player = list(filter(lambda x: x.uid == uid, self.players))
            odered_list_player.append(player)
        self.gameView[Constant.MATCH_MAKING] = False
        self.gameView[Constant.GAME] = True
        self.players = odered_list_player
    
    def player_turn(self, data):
        if data['uid'] == self.uid:
            self.myTurn = True
        else:
            self.myTurn = False
    
    def player_dice_move(self, data):
        player: Player = list(filter(lambda x: x.uid == data["uid"], self.players))
        self.dice.setServResp(data["value"])
        player.piece.move(data["value"], data["position"])

    def game_end(self, data):
        self.gameView[Constant.GAME] = False
        self.gameView[Constant.WINNER] = True
        player = list(filter(lambda x: x.uid == data["uid"], self.players))
        self.playerWinner = player

    def update_players(self, data):
        newList = []
        for dataPlayer in data["players"]:
            player: Player = list(filter(lambda x: x.uid == dataPlayer["uid"], self.players))
            newList.append(player[0])
        self.players = newList    

    def defaultFct():
        print("event not known !")

    def event(self, data):
        switcher = {
            "ME": self.me,
            "LIST_PLAYERS": self.list_player,
        }
        if (self.gameView.index(True) >= Constant.MATCH_MAKING):
            switcher.update({
                "GAME_START": self.game_start,
            })
        if (self.gameView.index(True) >= Constant.GAME):
            switcher.update({    
                "PLAYER_TURN": self.player_turn,
                "PLAYER_ROLLING_DICE": self.dice.roll_dice_animation,
                "PLAYER_DICE": self.player_dice_move,
                "GAME_END": self.game_end,
                "UPDATE_PLAYERS": self.update_players
            })
        switcher.update({"DEFAULT": self.defaultFct})
        print(data['event'])
        print(data['data'])
        switcher.get(data['event'], "DEFAULT")(data["data"])

Game()