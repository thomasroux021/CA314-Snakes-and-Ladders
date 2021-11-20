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
from Container.PlayerView import PlayerView
from Snake import Snake
from Ladder import Ladder

from Utils import Utils
from QueueView import QueueView

load_dotenv()

class Game:
    def __init__(self) -> None:
        Client.getInstance().init(self.event)
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.uid = None
        self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption('Snakes And Ladders')

        self.gameView = [False, False, True, False]
        self.gameRun = True
        self.myTurn = False

        self.clock = pygame.time.Clock()
        self.dice = Dice(self.gameDisplay)
        self.board = Board(self.gameDisplay)

        self.playerWinner = None

        self.players: List[Player] = []
        self.snakes: List[Snake] = []
        self.ladders: List[Ladder] = []

        #View
        self.queue_view = QueueView(self.players, self.gameDisplay, self.uid)
        self.players_view: List[PlayerView] = []

        self.draw()


    def draw(self):
        try:
            while self.gameRun:
                self.gameDisplay.fill(Constant.back)
                Client.getInstance().receive()
                event_list = pygame.event.get()
                for event in event_list:
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        self.gameRun = False
                #if (self.gameView.index(True) == Constant.MENU):
                if (self.gameView.index(True) == Constant.MATCH_MAKING):
                    self.queue_view.draw(event_list, self.go_out_from_queue)
                elif (self.gameView.index(True) == Constant.GAME):
                    self.board.draw()
                    self.dice.draw()
                    for player_view in self.players_view:
                        player_view.draw()
                #elif (self.gameView.index(True) == Constant.WINNER):
                pygame.display.update()
                self.clock.tick(60)
            pygame.quit()
        except KeyboardInterrupt:
            pygame.quit()
            sys.exit()

    def go_out_from_queue(self):
        self.gameView[Constant.MATCH_MAKING] = False
        self.gameView[Constant.MENU] = True
        Client.getInstance().send(Utils.all("REMOVE_PLAYER", {}))

    def me(self, data):
        self.uid = data['uid']
        self.queue_view.set_my_uid(self.uid)
        Client.getInstance().send(Utils.all("ADD_PLAYER", {'username': 'Remi', 'uid': self.uid}))
    
    def list_player(self, data):
        for dataPlayer in data["players"]:
            player = list(filter(lambda x: x.uid == dataPlayer["uid"], self.players))
            if (not player):
                newPiece = Piece(self.gameDisplay, dataPlayer["color"], self.board, dataPlayer["uid"])
                self.players.append(Player(dataPlayer["uid"], dataPlayer["username"], newPiece))
                self.queue_view.update_player(self.players)
                
                self.players_view.clear()
                ## Remove
                for idx,player in enumerate(self.players):
                    self.players_view.append(PlayerView(self.gameDisplay, player, 630, idx * 70 + 320, self.uid))
                ## end Remove
                
                ## to uncomment
                # self.gameView[Constant.MENU] = False
                # self.gameView[Constant.MATCH_MAKING] = True
                ## end to uncomment
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
        for idx, player in enumerate(self.players):
            self.players_view.append(PlayerView(self.gameDisplay, player, 630, idx * 70 + 320, self.uid))
    
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
        for actual_player in self.players:
            if not actual_player in newList:
                self.board.remove_piece(actual_player.get_piece())
        self.players = newList
        self.queue_view.update_player(self.players)
        self.players_view.clear()
        for idx, player in enumerate(self.players):
            self.players_view.append(PlayerView(self.gameDisplay, player, 630, idx * 70 + 320, self.uid))

    def defaultFct(self, data = None):
        print("event not known !")

    def event(self, data):
        switcher = {
            "ME": self.me,
            "LIST_PLAYERS": self.list_player,
        }
        if (self.gameView.index(True) >= Constant.MATCH_MAKING):
            switcher.update({
                "GAME_START": self.game_start,
                "UPDATE_PLAYERS": self.update_players
            })
        if (self.gameView.index(True) >= Constant.GAME):
            switcher.update({    
                "PLAYER_TURN": self.player_turn,
                "PLAYER_ROLLING_DICE": self.dice.roll_dice_animation,
                "PLAYER_DICE": self.player_dice_move,
                "GAME_END": self.game_end
            })
        switcher.update({"DEFAULT": self.defaultFct})
        print(data['event'])
        print(data['data'])
        # try:
        switcher.get(data['event'], "DEFAULT")(data["data"])
        # except:
        #     self.defaultFct()
Game()