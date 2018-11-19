import pygame
from gameObject import GameObject

class Grunt(GameObject):
    score = 50
    
    @staticmethod
    def init(screenWidth):
        Grunt.size = int(screenWidth * 0.06) # 6% of the screenWidth
        Grunt.image = pygame.transform.scale(\
        pygame.image.load('images/grunt.png').convert_alpha(), (Grunt.size, Grunt.size))

    def __init__(self, x, y):
        super(Grunt, self).__init__(x, y, Grunt.image, Grunt.size)
