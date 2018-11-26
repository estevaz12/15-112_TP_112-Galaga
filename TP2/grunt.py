import pygame
import random
from enemy import Enemy
from enemyBullet import eBullet

class Grunt(Enemy):
    score = 50

    @staticmethod
    def init(screenWidth, image):
        Grunt.size = int(screenWidth * 0.06) # 6% of the screenWidth
        Grunt.image = pygame.transform.scale(\
        pygame.image.load(image).convert_alpha(), (Grunt.size, Grunt.size))

    def __init__(self, x, y):
        super(Grunt, self).__init__(x, y, Grunt.image, Grunt.size)

    def shoot(self, ship):
        a = ship.x - ship.size * 5
        b = ship.x + ship.size * 5
        x = random.randint(a, b)
        return eBullet(x, ship.y, self)

    # def update(self, flap, screenWidth):
    #     if flap:
    #         Grunt.init(screenWidth, 'images/grunt2.png')
    #         self.__init__(self.x, self.y)
    #     else:
    #         Grunt.init(screenWidth, 'images/grunt.png')
    #         self.__init__(self.x, self.y)
    #     self.updateRect()
