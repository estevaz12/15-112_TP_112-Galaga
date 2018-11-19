import pygame
from gameObject import GameObject

'''
Concept from GameObject.py and Ship.py by Lukas Peraza
https://github.com/LBPeraza/Pygame-Asteroids/tree/master/Asteroids
'''

class Ship(GameObject):
    @staticmethod
    def init(screenWidth):
        Ship.size = int(screenWidth * 0.08) # 8% of the screen width
        Ship.shipImage = pygame.transform.scale(\
        pygame.image.load('images/ship.png').convert_alpha(), (Ship.size, Ship.size))

    def __init__(self, x, y):
        super(Ship, self).__init__(x, y, Ship.shipImage, Ship.size)
        self.speed = 4

    def update(self, keysDown, screenWidth):
        # move left or right but don't go off the screen
        if self.rect.left > 0:
            if keysDown(pygame.K_LEFT):
                self.x += self.speed * -1
        else:
            if keysDown(pygame.K_RIGHT):
                self.x += self.speed

        if self.rect.right < screenWidth:
            if keysDown(pygame.K_RIGHT):
                self.x += self.speed
        else:
            if keysDown(pygame.K_LEFT):
                self.x += self.speed * -1
        self.updateRect()
