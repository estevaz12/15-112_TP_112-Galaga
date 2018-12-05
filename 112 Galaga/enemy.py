import pygame
import math
import random
from gameObject import GameObject
from bullet import eBullet

class Enemy(GameObject):
    def __init__(self, x, y, image, size, finalX, finalY, dir="None"):
        super(Enemy, self).__init__(x, y, image, size)
        self.initX = self.x
        self.initY = self.y
        self.finalX = finalX
        self.finalY = finalY
        self.path = []
        self.gotPath = False
        self.entPath = []
        self.entering = True
        self.eDir = dir
        self.diving = None

    def entrancePath(self, width):
        angle = math.radians(270)
        r = 75
        midX = None
        if self.eDir == "left":
            dir = 1
            midX = (self.initX + width) / 2
        elif self.eDir == "right":
            dir = -1
            midX = width / 2
        midY = self.initY # Because why doesn't change for now
        cX, cY = midX, midY - r

        incr = (2 * math.pi) / self.numP

        # Make linear path
        for i in range(1, self.numP + 1):
            x = self.initX + ((i/self.numP) * (midX - self.initX))
            y = self.initY
            self.entPath.append((x, y))

        # Make circular path
        for i in range(self.numP):
            x = cX - r * math.cos((incr * i) - angle) * dir
            y = cY + r * math.sin((incr * i) - angle)
            self.entPath.append((x, y))

        # Finish path
        for i in range(1, self.numP + 1):
            endP = None
            if self.eDir == "left": endP = width * 2
            elif self.eDir == "right": endP = -width
            x = midX + ((i/self.numP) * ((endP) - midX))
            y = midY
            self.entPath.append((x, y))

    def generatePath(self, ship): # to ship
        o = ship.x - self.initX # opposite
        a = ship.y - self.initY # adjacent
        angle = math.atan(o/a)

        dir = random.choice([-1, 1])

        r = random.randint(self.size, 100)
        midX = (self.initX + ship.x) / 2
        midY = (self.initY + ship.y) / 2
        startP = (midX + r * math.cos(-angle), midY + r * math.sin(-angle)) # For the circle

        incr = (2 * math.pi) / self.numP

        # Make linear path
        for i in range(1, self.numP + 1):
            x = self.initX + ((i/self.numP) * (startP[0] - self.initX))
            y = self.initY + ((i/self.numP) * (startP[1] - self.initY))
            self.path.append((x, y))

        # Make circular path
        for i in range(self.numP):
            x = midX + r * math.cos((incr * i) - angle)
            y = midY + r * math.sin((incr * i) - angle) * dir
            self.path.append((x, y))

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
    def update(self, ship, width):
        if self.entering:
            if self.gotPath == False:
                self.entrancePath(width)
                self.gotPath = True
            if len(self.entPath) != 0:
                self.x = self.entPath[0][0]
                self.y = self.entPath[0][1]
                self.entPath = self.entPath[1:]
            else: # Go to formation
                self.initX = self.finalX
                self.initY = self.finalY
                newPos = self.moveBackToPos()
                if newPos:
                    self.x = self.x + newPos[0] * self.speed
                    self.y = self.y + newPos[1] * self.speed
                if self.y <= self.finalY:
                    self.x, self.y = self.finalX, self.finalY
                    self.entering = False
                    self.gotPath = False
        else:
            if self.diving:
                if self.gotPath == False:
                    self.generatePath(ship)
                    self.gotPath = True
                if len(self.path) != 0:
                    self.x = self.path[0][0]
                    self.y = self.path[0][1]
                    self.path = self.path[1:]
                else:
                    # move enemy towards player
                    newPos = self.moveTowardsShip(ship)
                    if newPos: #if not ZeroDivisonError
                        self.x = self.x + newPos[0] * self.speed
                        self.y = self.y + newPos[1] * self.speed
                    if self.y >= ship.y:
                        self.diving = False
                        self.gotPath = False
            elif self.diving == False:
                oldPos = self.moveBackToPos()
                if oldPos:
                    self.x = self.x + oldPos[0] * self.speed
                    self.y = self.y + oldPos[1] * self.speed
                if self.y <= self.initY:
                    self.x, self.y = self.initX, self.initY
                    self.diving = None

        self.updateRect()

class Grunt(Enemy):
    score = 50

    @staticmethod
    def init(screenWidth, image):
        Grunt.size = int(screenWidth * 0.06) # 6% of the screenWidth
        Grunt.image = pygame.transform.scale(\
        pygame.image.load(image).convert_alpha(), (Grunt.size, Grunt.size))

    def __init__(self, x, y, difficulty, finalX, finalY, dir="left"):
        super(Grunt, self).__init__(x, y, Grunt.image, Grunt.size, finalX, finalY, dir)
        self.speed = 4
        self.numP = 45
        if difficulty == "easy":
            self.speed = 4
            self.numP = 45
        elif difficulty == "normal":
            self.speed = 5
            self.numP = 40
        elif difficulty == "hard":
            self.speed = 6
            self.numP = 35

    def shoot(self, x, y, shipSize, difficulty):
        return eBullet(x, y, self, difficulty)

class Guard(Enemy):
    score = 80

    @staticmethod
    def init(screenWidth, image):
        Guard.size = int(screenWidth * 0.06) # 6% of the screenWidth
        Guard.image = pygame.transform.scale(\
        pygame.image.load(image).convert_alpha(), (Guard.size, Guard.size))

    def __init__(self, x, y, difficulty, finalX, finalY, dir="right"):
        super(Guard, self).__init__(x, y, Guard.image, Guard.size, finalX, finalY, dir)
        self.speed = 5
        self.numP = 50
        if difficulty == "easy":
            self.speed = 5
            self.numP = 50
        elif difficulty == "normal":
            self.speed = 6
            self.numP = 40
        elif difficulty == "hard":
            self.speed = 7
            self.numP = 30

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

class Boss(Enemy):
    score = 150

    @staticmethod
    def init(screenWidth, image):
        Boss.size = int(screenWidth * 0.07) # 7% of the screenWidth
        Boss.image = pygame.transform.scale(\
        pygame.image.load(image).convert_alpha(), (Boss.size, Boss.size))

    def __init__(self, x, y, difficulty, finalX, finalY, dir="left", lives=1, \
                diving=False, entering=True):
        super(Boss, self).__init__(x, y, Boss.image, Boss.size, finalX, finalY, dir)
        self.lives = lives
        self.diving = diving
        self.entering = entering
        self.speed = 7
        self.numP = 30
        if difficulty == "easy":
            self.speed = 7
            self.numP = 30
        elif difficulty == "normal":
            self.speed = 8
            self.numP = 25
        elif difficulty == "hard":
            self.speed = 9
            self.numP = 20

    def hurt(self, screenWidth, difficulty, diving, entering):
        if self.lives > 0:
            Boss.init(screenWidth, 'images/boss-hurt.png')
            return Boss(self.x, self.y, difficulty, self.finalX, self.finalY, self.eDir, \
                        self.lives-1, diving, entering)
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
