from typing import List
import pygame
import os
from Client import *
from dotenv import load_dotenv

from Board import *
from Constant import *
from Piece import *
from Player import *
from Dice import *

load_dotenv()

class Game():
    def __init__(self) -> None:
        pygame.init()
        # Client.getInstance().init()
        self.display_width = 800
        self.display_height = 600
        self.uid = None
        self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption('Snake And Ladder')

        self.gameRun = True
        self.myTurn = False

        self.clock = pygame.time.Clock()
        self.dice = Dice(self.gameDisplay)
        self.board = Board(self.gameDisplay)

        self.players: List[Player] = []
        self.pieces: List[Piece.Piece] = [
            Piece.Piece(self.gameDisplay, (0,211,255), self.board, 1), 
            Piece.Piece(self.gameDisplay, (255,121,191), self.board, 2),
            Piece.Piece(self.gameDisplay, (211,0,255), self.board, 3), 
            Piece.Piece(self.gameDisplay, (191,121,222), self.board, 4)
        ]
        #Client.getInstance().receive()
        self.draw()


    def draw(self):
        self.gameDisplay.fill(Constant.back)
        while self.gameRun:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameRun = False
            self.board.draw()
            self.dice.draw()
            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()

    def update_players(self, data, uuid):
        for dataPlayer in data["players"]:
            player = filter(lambda x: x.uid == data["uid"], self.players)
            if (not player):
                self.players.append(Player(data["uid"], dataPlayer["name"]))
            
    def update_pieces(self, data, addr):
        for datapiece in data["pieces"]:
            player: Player = filter(lambda x: x.uid == data["uid"], self.players)
            piece = filter(lambda x: x.userUid == data["uid"], self.pieces)
            if not piece:
                newPiece = Piece(self.gameDisplay, (0,211,255), self.board, data["uid"])
                self.pieces.append(newPiece)
                player.set_piece(newPiece)
                break
    
    def start_game(self):
        return 0
    
    def show_roll_dice(self, data, addr):
        # self.dice.
        # return value
        return

    def turn_to(self, data, addr):
        if (data['uid'] == self.uid):
            self.myTurn = True

    def end_turn(self, data):
        if (data['uid'] == self.uid):
            self.myTurn = False

    def me(self, data):
        self.uid = data['uid']

    def event(self, data, addr):
        switcher = {
            "UPDATE_PLAYER": self.update_players,
            "UPDATE_PIECE": self.update_pieces,
            "ROLL_DICE": self.show_roll_dice,
            "VALUE_DICE_ROLL": self.show_roll_dice,
            "START_GAME": self.start_game,
            "TURN_TO": self.turn_to,
            "END_TURN": self.end_turn,
            "ME": self.me
        }
        switcher.get(data["type"], "default")(data["data"], addr)

Game()