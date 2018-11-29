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

    def __init__(self, x, y, difficulty):
        super(Grunt, self).__init__(x, y, Grunt.image, Grunt.size)
        self.speed = 4
        if difficulty == "easy":
            self.speed = 4
        elif difficulty == "normal":
            self.speed = 5
        elif difficulty == "hard":
            self.speed = 6

    def shoot(self, x, y, shipSize, difficulty):
        return eBullet(x, y, self, difficulty)

    # def update(self, flap, screenWidth):
    #     if flap:
    #         Grunt.init(screenWidth, 'images/grunt2.png')
    #         self.__init__(self.x, self.y)
    #     else:
    #         Grunt.init(screenWidth, 'images/grunt.png')
    #         self.__init__(self.x, self.y)
    #     self.updateRect()
