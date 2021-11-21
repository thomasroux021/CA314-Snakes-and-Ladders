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
from Menu import *
from Container.Text import Text

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
        pygame.font.init()

        self.gameView = [True, False, False, False]
        self.gameRun = True
        self.myTurn = False
        self.turnPlayer: PlayerView = None
        

        self.clock = pygame.time.Clock()
        self.dice = Dice(self.gameDisplay)
        self.board = Board(self.gameDisplay)
        self.menu = Menu(self.gameDisplay, self.quit_game, self.join_queue)

        self.playerWinner = None

        self.players: List[Player] = []
        self.snakes: List[Snake] = []
        self.ladders: List[Ladder] = []

        #View
        self.queue_view = QueueView(self.players, self.gameDisplay, self.uid)
        self.players_view: List[PlayerView] = []
        self.turnText = Text(self.gameDisplay, "Turn", 710, 25, 50)
        self.listPlayerText = Text(self.gameDisplay, "List Player", 700, 320, 40)

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
                    if (self.gameView.index(True) == Constant.MENU):
                        self.menu.handle_event(event)
                    if (self.gameView.index(True) == Constant.GAME):
                        self.dice.event(event, self.rollDice)

                if (self.gameView.index(True) == Constant.MENU):
                    self.menu.draw()
                elif (self.gameView.index(True) == Constant.MATCH_MAKING):
                    self.queue_view.draw(event_list, self.go_out_from_queue)
                elif (self.gameView.index(True) == Constant.GAME):
                    self.board.draw()
                    if (self.turnPlayer):
                        self.turnText.draw()
                        self.turnPlayer.draw()
                    self.dice.draw()
                    self.listPlayerText.draw()
                    for player_view in self.players_view:
                        player_view.draw()
                #elif (self.gameView.index(True) == Constant.WINNER):
                pygame.display.update()
                self.clock.tick(60)
            pygame.quit()
        except KeyboardInterrupt:
            pygame.quit()
            sys.exit()
    
    def rollDice(self):
        if (self.myTurn):
            Client.getInstance().send(Utils.all("ROLL_DICE", {}))
            self.myTurn = False
        else:
            print("Not your turn !")

    def go_out_from_queue(self):
        self.gameView[Constant.MATCH_MAKING] = False
        self.gameView[Constant.MENU] = True
        Client.getInstance().send(Utils.all("REMOVE_PLAYER", {}))

    def me(self, data):
        self.uid = data['uid']
        self.queue_view.set_my_uid(self.uid)
    
    def quit_game(self):
        self.gameRun = False

    def join_queue(self):
        self.gameView[Constant.MENU] = False
        self.gameView[Constant.MATCH_MAKING] = True
        Client.getInstance().send(Utils.all("ADD_PLAYER", {'username': self.menu.get_username(), 'uid': self.uid}))
    
    def list_player(self, data):
        for dataPlayer in data["players"]:
            player = list(filter(lambda x: x.uid == dataPlayer["uid"], self.players))
            if (not player):
                newPiece = Piece(self.gameDisplay, dataPlayer["color"], self.board, dataPlayer["uid"])
                self.players.append(Player(dataPlayer["uid"], dataPlayer["username"], newPiece))
                self.queue_view.update_player(self.players)
            else:
                continue
    
    def game_start(self, data):
        self.board.event_add_snakes_ladders(data["snakes"], data["ladders"])
        odered_list_player = []
        for uid in data["order"]:
            player = list(filter(lambda x: x.uid == uid, self.players))
            odered_list_player.append(player[0])
        self.gameView[Constant.MATCH_MAKING] = False
        self.gameView[Constant.GAME] = True
        self.players = odered_list_player
        for idx, player in enumerate(self.players):
            self.players_view.append(PlayerView(self.gameDisplay, player, 630, idx * 70 + 370, self.uid))
    
    def player_turn(self, data):
        if data['uid'] == self.uid:
            self.myTurn = True
        else:
            self.myTurn = False
        player = list(filter(lambda x: x.uid == data['uid'], self.players))[0]
        self.turnPlayer = PlayerView(self.gameDisplay, player, 630, 65, self.uid)
    
    def player_dice_move(self, data):
        player: Player = list(filter(lambda x: x.uid == data["uid"], self.players))
        self.dice.setServResp(data["value"])
        player[0].piece.move(data["value"], data["position"])
        self.dice.reset()

    def game_end(self, data):
        self.gameView[Constant.WINNER] = True
        player = list(filter(lambda x: x.uid == data["uid"], self.players))
        self.playerWinner = player[0]

    def update_players(self, data):
        newList = []
        for dataPlayer in data["players"]:
            player: Player = list(filter(lambda x: x.uid == dataPlayer["uid"], self.players))
            newList.append(player[0])
        for actual_player in self.players:
            if not actual_player in newList:
                if (self.gameView[Constant.GAME]):
                    self.board.remove_piece(actual_player.get_piece())
                self.players.remove(actual_player)
        self.queue_view.update_player(self.players)
        self.players_view.clear()
        for idx, player in enumerate(self.players):
            self.players_view.append(PlayerView(self.gameDisplay, player, 630, idx * 70 + 370, self.uid))

    def defaultFct(self, data = None):
        print("event not known !")

    def event(self, data):
        switcher = {
            "ME": self.me,
            "LIST_PLAYERS": self.list_player,
            "UPDATE_PLAYERS": self.update_players
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