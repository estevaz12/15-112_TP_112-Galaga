import pygame
import random
from pygameGame import PygameGame
from ship import Ship
from shipBullet import sBullet
from enemyBullet import eBullet
from boss import Boss
from guard import Guard
from grunt import Grunt
from explosions import *


class GamePlay(PygameGame):
    def init(self):
        self.margin = self.width * 0.12
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
        self.startY = self.height - self.margin
        self.shipGroup = pygame.sprite.Group(Ship(self.startX, self.startY))

        # Ship lives
        imageSize = self.shipGroup.sprites()[0].size // 2
        livesImage = pygame.transform.scale(\
                          pygame.image.load('images/ship-lives.png').convert_alpha(),\
                                           (imageSize, imageSize))
        self.shipLives = []
        for i in range(self.shipGroup.sprites()[0].lives):
            self.shipLives.append(livesImage)

        # Explosions
        self.shipExpl = pygame.sprite.Group()
        self.enemyExpl = pygame.sprite.Group()

        col = self.width//10
        self.enemies = pygame.sprite.Group()

        # Boss
        Boss.init(self.width, 'images/boss.png')
        wB, hB = Boss.image.get_size()
        for i in range(3, 7):
            x = i * col + wB/2
            y = self.margin
            self.enemies.add(Boss(x, y))

        # Guards
        Guard.init(self.width, 'images/guard.png')
        for i in range(1, 9):
            for j in range(2, 4):
                x = i * col + wB/2 + 1 # centered based on boss
                y = self.margin/2 + offset * j
                self.enemies.add(Guard(x, y))

        # Grunts
        Grunt.init(self.width, 'images/grunt.png')
        for i in range(10):
            for j in range(4, 6):
                x = i * col + wB/2 + 1 # centered based on boss
                y = self.margin/2 + offset * j
                self.enemies.add(Grunt(x, y))

        self.flap = False

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
        if not (self.won or self.gameOver):
            if keyCode == pygame.K_SPACE and len(self.shipBullets.sprites()) < 3:
                sBullet.init()
                ship = self.shipGroup.sprites()[0]
                self.shipBullets.add(sBullet(ship.x, ship.y-(ship.height/2)))

    def timerFired(self, dt):
        self.time += 1
        factor = 50
        if self.time % 100 == 0:
            factor = random.choice([25, 50, 100])

        self.shipGroup.update(self.isKeyPressed, self.width)
        self.shipBullets.update()
        self.enemyBullets.update()
        self.shipExpl.update()
        self.enemyExpl.update()
        # if self.time % 100 == 0:
        #     self.enemies.update(self.flap, self.width)
        #     self.flap = not(self.flap)

        if not(self.gameOver):

            ship = self.shipGroup.sprites()[0]
            if self.time % factor == 0:
                enemyLst = self.enemies.sprites()
                if len(enemyLst) != 0:
                    numEnemies = random.randint(2, 4)
                    if len(enemyLst) > numEnemies:
                        enemy = random.sample(enemyLst, numEnemies)
                        eBullet.init()
                        self.enemyBullets.add(e.shoot(ship) for e in enemy)
                    else:
                        enemy = random.choice(enemyLst)
                        eBullet.init()
                        self.enemyBullets.add(enemy.shoot(ship))

            for enemy in pygame.sprite.groupcollide(self.enemies, self.shipBullets, \
                True, True, pygame.sprite.collide_circle):
                if isinstance(enemy, Boss) and enemy.lives > 0:
                    self.enemies.add(enemy.hurt(self.width))
                else:
                    eExplosion.init(self.width)
                    expl = eExplosion(enemy.rect.center)
                    self.enemyExpl.add(expl)
                    self.score += enemy.score
                    self.scoreTxt = self.scoreFont.render(str(self.score), False, \
                                    (255,255,255), (0,0,0))

            if pygame.sprite.groupcollide(self.shipGroup, self.enemyBullets, \
                True, True, pygame.sprite.collide_circle):
                    sExplosion.init(self.width)
                    expl = sExplosion(ship.rect.center)
                    self.shipExpl.add(expl)
                    if ship.lives > 0:
                        self.shipGroup.add(ship.hurt(self.startX, self.startY))
                        self.shipLives.pop()
                    else:
                        self.gameOver = True

            if not(self.enemies):
                self.won = True

    def redrawAll(self, screen):
        # Draw 'score'
        w, h = self.text.get_size()
        alignTxt = self.width/2 - w
        screen.blit(self.text, (alignTxt, 0))
        # Draw score
        w, h = self.scoreTxt.get_size()
        alignScore = self.width/2
        screen.blit(self.scoreTxt, (alignScore, 0))

        # Draw lives
        for i in range(len(self.shipLives)):
            w, h = self.shipLives[0].get_size()
            cols = self.width // w
            x = i * cols + w/2
            y = self.height - (self.margin / 2)
            screen.blit(self.shipLives[i], (x, y))

        self.shipGroup.draw(screen)
        self.shipBullets.draw(screen)
        self.enemies.draw(screen)
        self.enemyBullets.draw(screen)
        self.shipExpl.draw(screen)
        self.enemyExpl.draw(screen)

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
