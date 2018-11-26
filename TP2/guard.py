import pygame
import random
from enemy import Enemy
from enemyBullet import eBullet

class Guard(Enemy):
    score = 80

    @staticmethod
    def init(screenWidth, image):
        Guard.size = int(screenWidth * 0.06) # 6% of the screenWidth
        Guard.image = pygame.transform.scale(\
        pygame.image.load(image).convert_alpha(), (Guard.size, Guard.size))

    def __init__(self, x, y):
        super(Guard, self).__init__(x, y, Guard.image, Guard.size)

    def shoot(self, ship):
        a = ship.x - ship.size * 3
        b = ship.x + ship.size * 3
        x1 = random.randint(a, b)
        x2 = random.randint(a, b)
        return [eBullet(x1, ship.y, self), eBullet(x2, ship.y, self)]
