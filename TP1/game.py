'''
Concept from Game.py by Lukas Peraza
https://github.com/LBPeraza/Pygame-Asteroids/tree/master/Asteroids
'''
import pygame
from pygameGame import PygameGame
from ship import Ship
from bullet import Bullet
from boss import Boss
from guard import Guard
from grunt import Grunt

class Game(PygameGame):
    def init(self):
        margin = self.width * 0.10
        pygame.font.init()

        self.score = 0

        # Ship
        Ship.init(self.width)
        self.shipGroup = pygame.sprite.Group(Ship(self.width/2, \
                                                  self.height - margin))
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
                y = margin * j
                self.enemies.add(Guard(x, y))

        # Grunts
        Grunt.init(self.width)
        for i in range(10):
            for j in range(4, 6):
                x = i * col + wB/2 + 1 # centered based on boss
                y = margin * j
                self.enemies.add(Grunt(x, y))

        self.bullets = pygame.sprite.Group()

    def keyPressed(self, keyCode, mod):
        if keyCode == pygame.K_SPACE:
            ship = self.shipGroup.sprites()[0]
            Bullet.init()
            self.bullets.add(Bullet(ship.x, ship.y-(ship.height/2)))

    def timerFired(self, dt):
        self.shipGroup.update(self.isKeyPressed, self.width)
        self.bullets.update(self.height)

        for enemy in pygame.sprite.groupcollide(self.enemies, self.bullets, \
            True, True,
            pygame.sprite.collide_circle):
            if isinstance(enemy, Boss) and enemy.lives > 0:
                self.enemies.add(enemy.hurt(self.width))
            else:
                self.score += enemy.score

    def redrawAll(self, screen):
        self.shipGroup.draw(screen)
        self.bullets.draw(screen)
        self.enemies.draw(screen)


Game(400, 500).run()

'''
For TP1:
- Start
- End
'''
