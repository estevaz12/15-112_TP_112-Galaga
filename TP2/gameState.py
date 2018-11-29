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
        self.introMusic = pygame.mixer.Sound('sounds/stage-intro.ogg')
        self.introTimer = 7
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
        Boss.init(self.width, 'images/boss.png')
        wB, hB = Boss.image.get_size()
        for i in range(3, 7):
            x = i * col + wB/2
            y = self.margin
            self.enemies.add(Boss(x, y, self.difficulty))

        # Guards
        Guard.init(self.width, 'images/guard.png')
        for i in range(1, 9):
            for j in range(2, 4):
                x = i * col + wB/2 + 1 # centered based on boss
                y = self.margin/2 + offset * j
                self.enemies.add(Guard(x, y, self.difficulty))

        # Grunts
        Grunt.init(self.width, 'images/grunt.png')
        for i in range(10):
            for j in range(4, 6):
                x = i * col + wB/2 + 1 # centered based on boss
                y = self.margin/2 + offset * j
                self.enemies.add(Grunt(x, y, self.difficulty))

        self.buckets = {}
        self.midBuckets = set() # middle of buckets
        for enemy in self.enemies:
            if isinstance(enemy, Grunt):
                enemyRect = enemy.rect
                x, y = enemyRect.topright
                cx = enemyRect.centerx
                self.buckets[x] = []
                self.midBuckets.add(cx)
        self.midBuckets = sorted(list(self.midBuckets))
        self.bucketsLst = sorted(self.buckets.keys())

        # self.flap = False

        self.shipBullets = pygame.sprite.Group()
        self.shipSound = pygame.mixer.Sound('sounds/ship-shot.ogg')
        self.enemyBullets = pygame.sprite.Group()

        stateFont = pygame.font.SysFont('emulogic', 20)

        self.gameOver = False
        self.gOMusic = pygame.mixer.Sound('sounds/game-over.ogg')
        # game over text
        self.gO = stateFont.render('GAME OVER', False, (255, 0, 0))

        self.won = False
        self.wonMusic = pygame.mixer.Sound('sounds/game-won.ogg')
        # wining text
        self.win = stateFont.render('YOU WON', False, (0,255,255))

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
        else:
            if keyCode == pygame.K_r:
                self.state = "start"
                pygame.mixer.stop()
                GamePlay.init(self)

    def timerFired(self, dt):
        self.time += 1

        if self.intro:
            if self.playedIntro == False:
                self.introMusic.play()
                self.playedIntro = True
            if self.introTimer > 0:
                if self.time % 50 == 0:
                    self.introTimer -= 1
            else: self.intro = False

        if self.respawn:
            self.shipGroup.update(self.isKeyPressed, self.width, self.buckets)
        self.shipBullets.update()

        if self.intro == False:
            self.enemyBullets.update()
            self.shipExpl.update()
            self.enemyExpl.update()
            # if self.time % 100 == 0:
            #     self.enemies.update(self.flap, self.width)
            #     self.flap = not(self.flap)

            if not(self.gameOver):

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

                self.enemies.update(ship)

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
                    if len(enemyLst) != 0: # and len(self.enemyBullets.sprites()) < 3:
                        if self.time % 50 == 0:
                            # numEnemies = random.randint(1, 3)
                            # if len(enemyLst) > numEnemies:
                            #     enemy = random.sample(enemyLst, numEnemies)
                            #     eBullet.init()
                            #     self.enemyBullets.add(e.shoot(x, y, ship.size) for e in enemy)
                            # else:
                            enemy = random.choice(enemyLst)
                            eBullet.init()
                            self.enemyBullets.add(enemy.shoot(x, y, ship.size, self.difficulty))
                        if self.time % 200 == 0: # Every four seconds
                            enemy = random.choice(enemyLst)
                            self.divingSound.play()
                            enemy.diving = True


                    for enemy in pygame.sprite.groupcollide(self.enemies, self.shipBullets, \
                        True, True, pygame.sprite.collide_circle):
                        if isinstance(enemy, Boss) and enemy.lives > 0:
                            self.enemies.add(enemy.hurt(self.width, self.difficulty, enemy.diving))
                        else:
                            self.enemyDead.play()
                            if enemy.diving: enemy.score *= 2
                            elif enemy.diving == False: enemy.score //= 2
                            eExplosion.init(self.width)
                            expl = eExplosion(enemy.rect.center)
                            self.enemyExpl.add(expl)
                            self.score += enemy.score
                            self.scoreTxt = self.scoreFont.render(str(self.score), False, \
                                            (255,255,255), (0,0,0))

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

                if not(self.enemies):
                    self.won = True

            if self.won and self.playedMusic == False:
                self.wonMusic.play()
                self.playedMusic = True
            elif self.gameOver and self.playedMusic == False:
                self.gOMusic.play()
                self.playedMusic = True

            if self.won or self.gameOver:
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

        if (self.gameOver or self.won) and self.displayTxt:
            w2, h2 = self.restartTxt.get_size()
            alignX2 = (alignX + w) - w2/2
            alignY2 = (alignY + h + 20) - h2/2
            screen.blit(self.restartTxt, (alignX2, alignY2))
