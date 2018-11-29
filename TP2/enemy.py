import math
from gameObject import GameObject

class Enemy(GameObject):
    def __init__(self, x, y, image, size):
        super(Enemy, self).__init__(x, y, image, size)
        self.initX = self.x
        self.initY = self.y
        self.diving = None

    # From: https://python-forum.io/Thread-PyGame-Enemy-AI-and-collision-part-6
    # But modified
    def moveTowardsShip(self, ship):
        shipX = ship.x
        shipY = ship.y * 1.5
        c = math.sqrt((shipX - self.x) ** 2 + (shipY - self.y) ** 2)
        try:
            x = (shipX - self.x) / c
            y = (shipY - self.y) / c
        except ZeroDivisionError:
            return False
        return (x,y)

    # From: https://python-forum.io/Thread-PyGame-Enemy-AI-and-collision-part-6
    # But modified
    def moveBackToPos(self):
        c = math.sqrt((self.initX - self.x) ** 2 + (self.initY - self.y) ** 2)
        try:
            x = (self.initX - self.x) / c * 1.5
            y = (self.initY - self.y) / c * 1.5
        except ZeroDivisionError:
            return False
        return (x,y)

    # From: https://python-forum.io/Thread-PyGame-Enemy-AI-and-collision-part-6
    # But modified
    def update(self, ship):
        if self.diving:
            # move enemy towards player
            newPos = self.moveTowardsShip(ship)
            if newPos: #if not ZeroDivisonError
                self.x = self.x + newPos[0] * self.speed
                self.y = self.y + newPos[1] * self.speed
            if self.y >= ship.y:
                self.diving = False
        elif self.diving == False:
            oldPos = self.moveBackToPos()
            if oldPos:
                self.x = self.x + oldPos[0] * self.speed
                self.y = self.y + oldPos[1] * self.speed
            if self.y <= self.initY:
                self.x, self.y = self.initX, self.initY
                self.diving = None
        self.updateRect()
