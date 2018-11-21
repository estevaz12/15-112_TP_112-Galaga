from gameObject import GameObject
from enemyBullet import eBullet

class Enemy(GameObject):
    def __init__(self, x, y, image, size):
        super(Enemy, self).__init__(x, y, image, size)

    def shoot(self, ship):
        return eBullet(ship, self)
