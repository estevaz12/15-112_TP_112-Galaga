import pygame
from gameObject import GameObject

class Boss(GameObject):
    score = 150

    @staticmethod
    def init(screenWidth, image):
        Boss.size = int(screenWidth * 0.07) # 7% of the screenWidth
        Boss.image = pygame.transform.scale(\
        pygame.image.load(image).convert_alpha(), (Boss.size, Boss.size))

    def __init__(self, x, y, lives=1):
        super(Boss, self).__init__(x, y, Boss.image, Boss.size)
        self.lives = lives

    def hurt(self, screenWidth):
        if self.lives > 0:
            Boss.init(screenWidth, 'images/boss-hurt.png')
            return Boss(self.x, self.y, self.lives-1)
        else:
            return []
