'''
Concept from Game.py by Lukas Peraza
https://github.com/LBPeraza/Pygame-Asteroids/tree/master/Asteroids

To display font: https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
'''
import pygame
import random
from pygameGame import PygameGame
from ship import Ship
from shipBullet import sBullet
from enemyBullet import eBullet
from boss import Boss
from guard import Guard
from grunt import Grunt

class Game(PygameGame):
    def init(self):
        pygame.font.init()
        self.state = "start"

        # Start state

        self.logo = pygame.transform.scale(pygame.image.load('images/galaga-logo.png').convert_alpha(), \
                (int(self.height/2), int(self.width/2)))
        startFont = pygame.font.SysFont('emulogic', 15)
        self.startTxt = startFont.render("Press 'SPACE' to start.", False, \
                        (0,255,255))
        self.displayTxt = True

        # Game state
        margin = self.width * 0.12
        offset = self.width * 0.07 # For alien separation
        self.time = 0

        self.score = 0
        # For score text
        self.scoreFont = pygame.font.SysFont('emulogic', 15)
        self.text = self.scoreFont.render('Score ', False, (255,0,0), (0,0,0))
        self.scoreTxt = self.scoreFont.render(str(self.score), False, (255,255,255), (0,0,0))

        # Ship
        Ship.init(self.width)
        self.startX = self.width/2
        self.startY = self.height - margin
        self.shipGroup = pygame.sprite.Group(Ship(self.startX, self.startY))

        col = self.width//10
        self.enemies = pygame.sprite.Group()

        # Boss
        Boss.init(self.width, 'images/boss.png')
        wB, hB = Boss.image.get_size()
        for i in range(3, 7):
            x = i * col + wB/2
            y = margin
            self.enemies.add(Boss(x, y))

        # Guards
        Guard.init(self.width)
        for i in range(1, 9):
            for j in range(2, 4):
                x = i * col + wB/2 + 1 # centered based on boss
                y = margin/2 + offset * j
                self.enemies.add(Guard(x, y))

        # Grunts
        Grunt.init(self.width)
        for i in range(10):
            for j in range(4, 6):
                x = i * col + wB/2 + 1 # centered based on boss
                y = margin/2 + offset * j
                self.enemies.add(Grunt(x, y))

        self.shipBullets = pygame.sprite.Group()
        self.enemyBullets = pygame.sprite.Group()

        stateFont = pygame.font.SysFont('emulogic', 20)

        self.gameOver = False
        # game over text
        self.gO = stateFont.render('GAME OVER', False, (255, 0, 0))
        self.won = False
        # wining text
        self.win = stateFont.render('YOU WON', False, (0,255,255))

    def keyPressed(self, keyCode, mod):
        if self.state == "start":
            if keyCode == pygame.K_SPACE:
                self.state = 'game'
        elif self.state == "game":
            if not (self.won or self.gameOver):
                if keyCode == pygame.K_SPACE:
                    sBullet.init()
                    ship = self.shipGroup.sprites()[0]
                    self.shipBullets.add(sBullet(ship.x, ship.y-(ship.height/2)))

    def timerFired(self, dt):
        if self.state == "start":
            self.time += 1
            if self.time % 50 == 0: # every second
                self.displayTxt = not(self.displayTxt)
        elif self.state == "game":
            self.time += 1

            self.shipGroup.update(self.isKeyPressed, self.width)
            self.shipBullets.update()
            self.enemyBullets.update()

            if not(self.gameOver):
                # Enemies shoot every two seconds
                ship = self.shipGroup.sprites()[0]
                if self.time % 100 == 0: # every two seconds
                    enemyLst = self.enemies.sprites()
                    if len(enemyLst) != 0:
                        enemy = random.choice(enemyLst)
                        eBullet.init()
                        self.enemyBullets.add(enemy.shoot(ship))

                for enemy in pygame.sprite.groupcollide(self.enemies, self.shipBullets, \
                    True, True, pygame.sprite.collide_circle):
                    if isinstance(enemy, Boss) and enemy.lives > 0:
                        self.enemies.add(enemy.hurt(self.width))
                    else:
                        self.score += enemy.score
                        self.scoreTxt = self.scoreFont.render(str(self.score), False, \
                                        (255,255,255), (0,0,0))

                if pygame.sprite.groupcollide(self.shipGroup, self.enemyBullets, \
                    True, True, pygame.sprite.collide_circle):
                        if ship.lives > 0:
                            self.shipGroup.add(ship.hurt(self.startX, self.startY))
                        else:
                            self.gameOver = True

                if not(self.enemies):
                    self.won = True

    def redrawAll(self, screen):
        if self.state == "start":
            w, h = self.logo.get_size()
            alignX = self.width/2 - w/2
            alignY = self.height/2 - h/2
            screen.blit(self.logo, (alignX, alignY))

            if self.displayTxt:
                w2, h2 = self.startTxt.get_size()
                alignX2 = (alignX + w/2) - w2/2
                alignY2 = (alignY + h + 10) - h2/2
                screen.blit(self.startTxt, (alignX2, alignY2))
        elif self.state == "game":
            # Draw 'score'
            w, h = self.text.get_size()
            alignTxt = self.width/2 - w
            screen.blit(self.text, (alignTxt, 0))
            # Draw score
            w, h = self.scoreTxt.get_size()
            alignScore = self.width/2
            screen.blit(self.scoreTxt, (alignScore, 0))

            self.shipGroup.draw(screen)
            self.shipBullets.draw(screen)
            self.enemies.draw(screen)
            self.enemyBullets.draw(screen)

            # Draw winning text
            if self.won:
                w, h = self.text.get_size()
                alignX = self.width/2 - w + 20 # so it's centered
                alignY = self.height/2
                screen.blit(self.win, (alignX, alignY))

            if self.gameOver:
                w, h = self.text.get_size()
                alignX = self.width/2 - w # so it's centered
                alignY = self.height/2
                screen.blit(self.gO, (alignX, alignY))


Game(400, 500).run()
