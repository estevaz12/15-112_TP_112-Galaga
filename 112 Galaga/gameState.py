# Everything that has to do with the gameplay itself

import pygame
import random
from pygameGame import PygameGame
from ship import Ship
from bullet import *
from enemy import *
from explosions import *


class GamePlay(PygameGame):
    def init(self):
        self.introMusic = pygame.mixer.Sound('sounds/stage-intro.ogg')
        self.timer = 7
        self.playedIntro = False
        self.intro = True

        self.error = 3
        if self.difficulty == "easy":
            self.error = 3
        elif self.difficulty == "normal":
            self.error = 2
        elif self.difficulty == "hard":
            self.error = 1

        self.margin = self.width * 0.12
        offset = self.width * 0.07 # For alien separation
        self.time = 0

        self.score = 0
        self.timePlaying = 0.0
        # For score text
        self.scoreFont = pygame.font.SysFont('emulogic', 15)
        self.text = self.scoreFont.render('Time ', False, (255,0,0), (0,0,0))
        self.scoreTxt = self.scoreFont.render(str(self.timePlaying)+" s", False, (255,255,255), (0,0,0))

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

        self.deathTime = 0

        # Explosions
        self.shipExpl = pygame.sprite.Group()
        self.enemyExpl = pygame.sprite.Group()
        self.shipDead = pygame.mixer.Sound('sounds/explosion.ogg')
        self.enemyDead = pygame.mixer.Sound('sounds/enemy-dead.ogg')

        self.canShoot = True
        self.divingSound = pygame.mixer.Sound('sounds/enemy-diving.ogg')
        self.respawn = True

        col = self.width//10
        self.enemies = pygame.sprite.Group()

        # Boss
        self.bFP = [] # short for boss final position
        Boss.init(self.width, 'images/boss.png')
        wB, hB = Boss.image.get_size()
        for i in range(3, 7):
            x = i * col + wB/2
            y = self.margin
            self.bFP.append((x, y)) # Where they stop

        # Guards
        self.gdFP = [] # short for guard final position
        for row in range(8): self.gdFP += [[None]*2]
        self.gd = True # True = 1 for guards
        self.remGuards = []

        Guard.init(self.width, 'images/guard.png')
        for i in range(1, 9):
            for j in range(2, 4):
                x = i * col + wB/2 + 1 # centered based on boss
                y = self.margin/2 + offset * j
                self.gdFP[i-1][j-2] = (x, y) # Where they stop

        # Grunts
        self.gtFP = [] # short for grunt final position
        for row in range(10): self.gtFP += [[None]*2]
        self.gt = False # Fasle = 0 for grunts
        self.remGrunts = []

        Grunt.init(self.width, 'images/grunt.png')
        for i in range(10):
            for j in range(4, 6):
                x = i * col + wB/2 + 1 # centered based on boss
                y = self.margin/2 + offset * j
                self.gtFP[i][j-4] = (x, y) # Where they stop

        gWidth = Grunt.size
        self.buckets = {}
        self.midBuckets = set() # middle of buckets
        for e in self.gtFP:
            x = e[0][0]
            cx = x + gWidth/2
            self.buckets[x] = []
            self.midBuckets.add(cx)
        self.midBuckets = sorted(list(self.midBuckets))
        self.bucketsLst = sorted(self.buckets.keys())

        self.entrance = True
        self.dir = random.choice(["left", "right"])

        self.shipBullets = pygame.sprite.Group()
        self.shipSound = pygame.mixer.Sound('sounds/ship-shot.ogg')
        self.enemyBullets = pygame.sprite.Group()

        self.stateFont = pygame.font.SysFont('emulogic', 20)

        self.timerTxt = self.stateFont.render(str(self.timer), False, (0,255,255))

        self.gameOver = False
        self.gOMusic = pygame.mixer.Sound('sounds/game-over.ogg')
        # game over text
        self.gO = self.stateFont.render('GAME OVER', False, (255, 0, 0))

        self.won = False
        self.wonMusic = pygame.mixer.Sound('sounds/game-won.ogg')
        # wining text
        self.win = self.stateFont.render('YOU WON', False, (0,255,255))

        self.playedMusic = False

        self.restartFont = pygame.font.SysFont('emulogic', 15)
        self.restartTxt = self.restartFont.render("Press 'R' to restart.", False, \
                        (255,0,0))
        self.displayTxt = True

    def keyPressed(self, keyCode, mod):
        if not (self.won or self.gameOver) and self.canShoot:
            if keyCode == pygame.K_SPACE and len(self.shipBullets.sprites()) < 2:
                self.shipSound.play()
                sBullet.init()
                ship = self.shipGroup.sprites()[0]
                self.shipBullets.add(sBullet(ship.x, ship.y-(ship.height/2)))

    def timerFired(self, dt):
        self.time += 1

        if self.intro:
            if self.playedIntro == False:
                self.introMusic.play()
                self.playedIntro = True
            if self.timer > 0:
                if self.time % 50 == 0:
                    self.timer -= 1
                    self.timerTxt = self.stateFont.render(str(self.timer), False, (0,255,255))
            else:
                self.intro = False
                self.timer = 7

        if self.won:
            if self.timer > 0:
                if self.time % 50 == 0:
                    self.timer -= 1
            else:
                self.state = "score"
                self.timer = 7

        if self.respawn:
            self.shipGroup.update(self.isKeyPressed, self.width, self.buckets)
        self.shipBullets.update()

        if self.intro == False and self.won == False and self.gameOver == False \
            and self.canShoot:
            self.timePlaying += 1
            self.scoreTxt = self.scoreFont.render("%0.2f s" % (self.timePlaying/50),
                            False, (255,255,255), (0,0,0))

        if self.intro == False:
            self.enemyBullets.update()
            self.shipExpl.update()
            self.enemyExpl.update()

            if not(self.gameOver):

                # Spawn enemies
                if self.time % 10 == 0:
                    if self.difficulty == "easy":

                        if len(self.gtFP) != 0:

                            if self.dir == "left": w = -Grunt.size
                            elif self.dir == "right": w = self.width + Grunt.size

                            self.enemies.add(Grunt(w, self.height/1.5, self.difficulty, \
                                                  self.gtFP[0][0][0], self.gtFP[0][0][1], self.dir))
                            self.enemies.add(Grunt(w, self.height/1.5 + Grunt.size + 5, self.difficulty, \
                                                  self.gtFP[0][1][0], self.gtFP[0][1][1], self.dir))
                            self.gtFP = self.gtFP[1:]

                        elif len(self.gdFP) != 0:
                            if self.dir == "left":
                                w = self.width + Guard.size
                                d = "right"
                            elif self.dir == "right":
                                w = -Guard.size
                                d = "left"

                            self.enemies.add(Guard(w, self.height/1.5, self.difficulty, \
                                                  self.gdFP[0][0][0], self.gdFP[0][0][1], d))
                            self.enemies.add(Guard(w, self.height/1.5 + Guard.size + 5, self.difficulty, \
                                                  self.gdFP[0][1][0], self.gdFP[0][1][1], d))
                            self.gdFP = self.gdFP[1:]

                        elif len(self.bFP) != 0:
                            if self.dir == "left": w = -Boss.size
                            elif self.dir == "right": w = self.width + Boss.size

                            self.enemies.add(Boss(w, self.height/1.5, self.difficulty, \
                                                  self.bFP[0][0], self.bFP[0][1], self.dir))
                            self.bFP = self.bFP[1:]

                        else: self.entrance = False

                    elif self.difficulty == "normal":
                        if self.dir == "left": w1 = -Grunt.size
                        elif self.dir == "right": w1 = self.width + Grunt.size

                        if self.dir == "left":
                            w2 = self.width + Guard.size
                            d = "right"
                        elif self.dir == "right":
                            w2 = -Guard.size
                            d = "left"

                        if len(self.gtFP) != 0:

                            if len(self.gdFP) != 0:
                                self.enemies.add(Guard(w2, self.height/1.5, self.difficulty, \
                                                      self.gdFP[0][0][0], self.gdFP[0][0][1], d))
                                self.remGuards.append(self.gdFP[0].pop())
                                self.gdFP = self.gdFP[1:]

                            self.enemies.add(Grunt(w1, self.height/1.5 + Grunt.size + 5, self.difficulty, \
                                                  self.gtFP[0][1][0], self.gtFP[0][1][1], self.dir))
                            self.remGrunts.append(self.gtFP[0].pop(0))
                            self.gtFP = self.gtFP[1:]

                        elif len(self.remGrunts) != 0:
                            if len(self.remGuards) != 0:
                                self.enemies.add(Guard(w1, self.height/1.5, self.difficulty, \
                                                      self.remGuards[0][0], self.remGuards[0][1], self.dir))
                                self.remGuards = self.remGuards[1:]

                            self.enemies.add(Grunt(w2, self.height/1.5 + Grunt.size + 5, self.difficulty, \
                                                  self.remGrunts[0][0], self.remGrunts[0][1], d))
                            self.remGrunts = self.remGrunts[1:]

                        elif len(self.bFP) != 0:
                            if self.dir == "left": w = -Boss.size
                            elif self.dir == "right": w = self.width + Boss.size
                            self.enemies.add(Boss(w, self.height/1.5, self.difficulty, \
                                                  self.bFP[0][0], self.bFP[0][1], self.dir))
                            self.bFP = self.bFP[1:]
                        else: self.entrance = False
                    elif self.difficulty == "hard":
                        if self.dir == "left": w1 = -Grunt.size
                        elif self.dir == "right": w1 = self.width + Grunt.size

                        if self.dir == "left":
                            w2 = self.width + Guard.size
                            d = "right"
                        elif self.dir == "right":
                            w2 = -Guard.size
                            d = "left"

                        if len(self.gtFP) != 0:
                            if len(self.gdFP) != 0:
                                self.gd = not(self.gd)
                                if self.gd: h1 = self.height/1.5
                                else: h1 = self.height/1.5 + Grunt.size + 5
                                i = int(self.gd)
                                self.enemies.add(Guard(w1, h1, self.difficulty, \
                                                      self.gdFP[0][i][0], self.gdFP[0][i][1], self.dir))

                                self.remGuards.append(self.gdFP[0].pop(int(not(i))))
                                self.gdFP = self.gdFP[1:]

                            self.gt = not(self.gt)
                            if self.gt: h2 = self.height/1.5
                            else: h2 = self.height/1.5 + Grunt.size + 5
                            j = int(self.gt)
                            self.enemies.add(Grunt(w1, h2, self.difficulty, \
                                                  self.gtFP[0][j][0], self.gtFP[0][j][1], self.dir))

                            self.remGrunts.append(self.gtFP[0].pop(int(not(j))))
                            self.gtFP = self.gtFP[1:]

                        elif len(self.remGrunts) != 0:
                            if len(self.remGuards) != 0:
                                self.gd = not(self.gd)
                                if self.gd: h1 = self.height/1.5
                                else: h1 = self.height/1.5 + Grunt.size + 5
                                self.enemies.add(Guard(w2, h1, self.difficulty, \
                                                      self.remGuards[0][0], self.remGuards[0][1], d))
                                self.remGuards = self.remGuards[1:]

                            self.gt = not(self.gt)
                            if self.gt: h2 = self.height/1.5
                            else: h2 = self.height/1.5 + Grunt.size + 5
                            self.enemies.add(Grunt(w2, h2, self.difficulty, \
                                                  self.remGrunts[0][0], self.remGrunts[0][1], d))
                            self.remGrunts = self.remGrunts[1:]
                        elif len(self.bFP) != 0:
                            self.enemies.add(Boss(-Boss.size, self.height/1.5, self.difficulty, \
                                                  self.bFP[0][0], self.bFP[0][1]))
                            self.bFP = self.bFP[1:]
                        else: self.entrance = False

                ship = None
                bucket = None
                x = self.startX
                y = self.startY
                idx = None

                if len(self.shipGroup.sprites()) != 0:
                     ship = self.shipGroup.sprites()[0]
                     bucket = ship.getBucket(self.buckets, self.width)
                     i = self.bucketsLst.index(bucket)
                     left = self.buckets[bucket].count(-1)
                     right = self.buckets[bucket].count(1)
                     if left > right:
                         idx = i - self.error
                         if idx < 0:
                             idx = i
                         x = self.midBuckets[idx]
                     elif right > left:
                         idx = i + self.error
                         if idx >= len(self.bucketsLst):
                             idx = i
                         x = self.midBuckets[idx]
                     else:
                         idx = i
                         x = self.midBuckets[idx]

                self.enemies.update(ship, self.width)

                if self.canShoot == False:
                    self.deathTime += 1

                if self.deathTime != 0:
                    if self.deathTime % 75 == 0:
                        self.respawn = True
                    if self.deathTime % 150 == 0:
                        self.canShoot = True

                if self.canShoot:
                    ship = self.shipGroup.sprites()[0]
                    enemyLst = self.enemies.sprites()
                    if len(enemyLst) != 0:
                        if self.time % 50 == 0:
                            enemy = random.choice(enemyLst)
                            eBullet.init()
                            self.enemyBullets.add(enemy.shoot(x, y, ship.size, self.difficulty))
                        if enemyLst[-1].entering == False and self.time % 200 == 0: # Every four seconds
                            enemy = random.choice(enemyLst)
                            self.divingSound.play()
                            enemy.diving = True


                    for enemy in pygame.sprite.groupcollide(self.enemies, self.shipBullets, \
                        True, True, pygame.sprite.collide_circle):
                        if isinstance(enemy, Boss) and enemy.lives > 0:
                            self.enemies.add(enemy.hurt(self.width, self.difficulty, \
                                        enemy.diving, enemy.entering))
                        else:
                            self.enemyDead.play()
                            if enemy.diving: enemy.score *= 2
                            elif enemy.diving == False: enemy.score //= 2
                            eExplosion.init(self.width)
                            expl = eExplosion(enemy.rect.center)
                            self.enemyExpl.add(expl)
                            self.score += enemy.score

                    if pygame.sprite.groupcollide(self.shipGroup, self.enemyBullets, \
                       True, True, pygame.sprite.collide_circle):
                        self.shipDead.play()
                        sExplosion.init(self.width)
                        expl = sExplosion(ship.rect.center)
                        self.shipExpl.add(expl)
                        self.canShoot = False
                        self.respawn = False
                        self.enemyBullets.empty()
                        self.shipBullets.empty()
                        for e in self.enemies.sprites():
                            e.diving = False
                        if ship.lives > 0:
                            self.shipGroup.add(ship.hurt(self.startX, self.startY))
                            self.shipLives.pop()
                            self.deathTime = 0
                        else:
                            self.gameOver = True

                    for enemy in pygame.sprite.groupcollide(self.enemies, self.shipGroup, \
                        False, True, pygame.sprite.collide_circle):
                        self.shipDead.play()
                        sExplosion.init(self.width)
                        expl = sExplosion(ship.rect.center)
                        self.shipExpl.add(expl)
                        self.canShoot = False
                        self.respawn = False
                        self.enemyBullets.empty()
                        self.shipBullets.empty()
                        enemy.diving = False
                        if ship.lives > 0:
                            self.shipGroup.add(ship.hurt(self.startX, self.startY))
                            self.shipLives.pop()
                            self.deathTime = 0
                        else:
                            pygame.mixer.stop()
                            self.gameOver = True

                if self.entrance == False and not(self.enemies):
                    self.won = True

            if self.won and self.playedMusic == False:
                self.wonMusic.play()
                self.timePlaying /= 50 # Turn into seconds
                self.playedMusic = True
            elif self.gameOver and self.playedMusic == False:
                self.gOMusic.play()
                self.playedMusic = True

            if self.gameOver:
                if self.time % 50 == 0: # Every second
                    self.displayTxt = not(self.displayTxt)

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

        if self.intro:
            w, h = self.timerTxt.get_size()
            alignX = self.startX - w/2
            screen.blit(self.timerTxt, (alignX, self.height/2))

        if self.respawn:
            self.shipGroup.draw(screen)
        self.shipBullets.draw(screen)
        self.enemies.draw(screen)
        self.enemyBullets.draw(screen)
        self.shipExpl.draw(screen)
        self.enemyExpl.draw(screen)

        # Draw winning text
        w, h = 0, 0
        alignX, alignY = 0, 0
        if self.won:
            w, h = self.text.get_size()
            alignX = self.width/2 - w + 20 # so it's centered
            alignY = self.height/2
            screen.blit(self.win, (alignX, alignY))
            alignX -= 20

        if self.gameOver:
            w, h = self.text.get_size()
            alignX = self.width/2 - w # so it's centered
            alignY = self.height/2
            screen.blit(self.gO, (alignX, alignY))

        if self.gameOver and self.displayTxt:
            w2, h2 = self.restartTxt.get_size()
            alignX2 = (alignX + w) - w2/2
            alignY2 = (alignY + h + 20) - h2/2
            screen.blit(self.restartTxt, (alignX2, alignY2))
