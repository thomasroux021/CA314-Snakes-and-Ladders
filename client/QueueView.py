from typing import List
from Container.Text import Text
from Container.PlayerView import PlayerView
from Container.Image import Image
import pygame

from Constant import Constant
from Player import Player

class QueueView:
    def __init__(self, players, gameDisplay, myUid) -> None:
        self.game_display = gameDisplay
        self.playersViews: List[PlayerView] = []
        self.myUid = myUid
        self.players = players
        
        self.titleTxt = Text(self.game_display, "Waiting users...", x = 800 / 2, y = 100, size= 50)
        self.ladderImg = Image(self.game_display, "assets/ladder-big.png", 50, 120)
        self.snakeImg = Image(self.game_display, "assets/snake-big.png", 720, 120)
        self.update_player(players)

    def set_my_uid(self, myUid, players = None):
        self.myUid = myUid
        if players is None:
            self.update_player(self.players)
        else:
            self.update_player(players)
    
    def update_player(self, players: List[Player]):
        self.playersViews.clear()
        for idx, player in enumerate(players):
            isMe = self.myUid == player.uid
            self.playersViews.append(PlayerView(self.game_display, player, 800 / 2 - 100, idx * 100 + 180, self.myUid, isMe))

    def draw(self, event_list, go_out):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for playerView in self.playersViews:
                    blit = playerView.get_cross_blit()
                    if (blit and blit.collidepoint(pos)):
                        go_out()

        self.titleTxt.draw()
        for playerView in self.playersViews:
            playerView.draw()
        self.ladderImg.draw()
        self.snakeImg.draw()