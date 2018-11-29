import pygame
import random
import math
from enemy import Enemy
from enemyBullet import eBullet

class Guard(Enemy):
    score = 80

    @staticmethod
    def init(screenWidth, image):
        Guard.size = int(screenWidth * 0.06) # 6% of the screenWidth
        Guard.image = pygame.transform.scale(\
        pygame.image.load(image).convert_alpha(), (Guard.size, Guard.size))

    def __init__(self, x, y, difficulty):
        super(Guard, self).__init__(x, y, Guard.image, Guard.size)
        self.speed = 5
        if difficulty == "easy":
            self.speed = 5
        elif difficulty == "normal":
            self.speed = 6
        elif difficulty == "hard":
            self.speed = 7

    def shoot(self, x, y, shipSize, difficulty):
        a = x - shipSize * 2
        b = x + shipSize * 2
        x1 = random.randint(a, b)
        x2 = random.randint(a, b)
        return [eBullet(x1, y, self, difficulty), eBullet(x2, y, self, difficulty)]

    # From: https://python-forum.io/Thread-PyGame-Enemy-AI-and-collision-part-6
    # But modified
    def moveTowardsShip(self, ship):
        shipX = ship.x
        shipY = ship.y * 1.3
        c = math.sqrt((shipX - self.x) ** 2 + (shipY - self.y) ** 2)
        try:
            x = (shipX - self.x) / c
            y = (shipY - self.y) / c
        except ZeroDivisionError:
            return False
        return (x,y)
