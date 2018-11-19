import pygame
from gameObject import GameObject

class Guard(GameObject):
    score = 80
    
    @staticmethod
    def init(screenWidth):
        Guard.size = int(screenWidth * 0.06) # 6% of the screenWidth
        Guard.image = pygame.transform.scale(\
        pygame.image.load('images/guard.png').convert_alpha(), (Guard.size, Guard.size))

    def __init__(self, x, y):
        super(Guard, self).__init__(x, y, Guard.image, Guard.size)
