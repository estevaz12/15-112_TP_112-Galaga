import pygame
import random
import math
from enemy import Enemy
from enemyBullet import eBullet

class Boss(Enemy):
    score = 150

    @staticmethod
    def init(screenWidth, image):
        Boss.size = int(screenWidth * 0.07) # 7% of the screenWidth
        Boss.image = pygame.transform.scale(\
        pygame.image.load(image).convert_alpha(), (Boss.size, Boss.size))

    def __init__(self, x, y, difficulty, lives=1, diving=False):
        super(Boss, self).__init__(x, y, Boss.image, Boss.size)
        self.lives = lives
        self.diving = diving
        self.speed = 7
        if difficulty == "easy":
            self.speed = 7
        elif difficulty == "normal":
            self.speed = 8
        elif difficulty == "hard":
            self.speed = 9

    def hurt(self, screenWidth, difficulty, diving):
        if self.lives > 0:
            Boss.init(screenWidth, 'images/boss-hurt.png')
            return Boss(self.x, self.y, difficulty, self.lives-1, diving)
        else:
            return []

    def shoot(self, x, y, shipSize, difficulty):
        left = x - shipSize * 1.5
        mid = x
        right = x + shipSize * 1.5
        return [eBullet(left, y, self, difficulty), eBullet(mid, y, self, difficulty),\
                eBullet(right, y, self, difficulty)]

    # From: https://python-forum.io/Thread-PyGame-Enemy-AI-and-collision-part-6
    # But modified
    def moveTowardsShip(self, ship):
        shipX = ship.x
        shipY = ship.y * 1.1
        c = math.sqrt((shipX - self.x) ** 2 + (shipY - self.y) ** 2)
        try:
            x = (shipX - self.x) / c
            y = (shipY - self.y) / c
        except ZeroDivisionError:
            return False
        return (x,y)
