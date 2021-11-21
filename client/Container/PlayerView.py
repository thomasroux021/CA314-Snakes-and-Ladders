import math

from Player import *
from Container.Text import *

class PlayerView:
    def __init__(self, gameDisplay, player: Player, x, y, myUid, displayCross = False, sizeCirce = 25) -> None:
        self.x = x
        self.y = y
        self.player = player
        self.game_display = gameDisplay
        self.sizeCirce = sizeCirce
        self.myUid = myUid
        self.display_cross = displayCross

        
        username = self.player.name
        if (self.player.uid == myUid):
            username += " (me)"
        self.usernameText = Text(self.game_display, username, self.x + 100, self.y, 31 - math.ceil(1.6 * max(0, len(username) - 11)))
        self.crossText: Text = None
        if (self.display_cross):
            self.crossText = Text(self.game_display, "X", self.x + 180, self.y, 40, (255, 0, 0))

    def get_cross_blit(self):
        if (self.crossText):
            return self.crossText.get_blit()
        else:
            return None

    def draw(self):
        self.usernameText.draw()
        pygame.draw.circle(self.game_display, (self.player.piece.colour), (self.x, self.y), self.sizeCirce)
        if (self.display_cross):
            self.crossText.draw()


        