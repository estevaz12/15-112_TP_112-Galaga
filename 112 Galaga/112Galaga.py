'''
Concept from Game.py by Lukas Peraza
https://github.com/LBPeraza/Pygame-Asteroids/tree/master/Asteroids

To display font: https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
'''
import module_manager
module_manager.review()

import pygame
from pygameGame import PygameGame
from start import Start
from gameState import GamePlay
from scoreState import ScoreBoard

class Game(PygameGame):
    def init(self):
        pygame.font.init()
        pygame.mixer.init()
        self.state = "start"

        # Start state
        Start.init(self)
        # Game state
        GamePlay.init(self)
        # Score state
        ScoreBoard.init(self)

    def keyPressed(self, keyCode, mod):
        if self.state == "start":
            Start.keyPressed(self, keyCode, mod)
        elif self.state == "game":
            GamePlay.keyPressed(self, keyCode, mod)
        elif self.state == "score":
            ScoreBoard.keyPressed(self, keyCode, mod)

        if self.canShoot == False or self.gameOver or self.screen == "board":
            if keyCode == pygame.K_r:
                pygame.mixer.stop()
                Game.init(self)

    def timerFired(self, dt):
        if self.state == "start":
            Start.timerFired(self, dt)
        elif self.state == "game":
            GamePlay.timerFired(self, dt)
        elif self.state == "score":
            ScoreBoard.timerFired(self, dt)

    def redrawAll(self, screen):
        if self.state == "start":
            Start.redrawAll(self, screen)
        elif self.state == "game":
            GamePlay.redrawAll(self, screen)
        elif self.state == "score":
            ScoreBoard.redrawAll(self, screen)


Game(400, 500).run()
