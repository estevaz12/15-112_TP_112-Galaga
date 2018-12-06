# Creates the animation for explosions

import pygame
import os

'''
From: https://stackoverflow.com/questions/43432339/loading-image-of-explosion-when-collision-with-character-sprite-in-pygame
'''

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, images):
        super(Explosion, self).__init__()
        self.imageLst = images
        self.image = images[0]
        self.rect = self.image.get_rect(center=center)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 * 3

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
        if self.frame == len(self.imageLst):
            self.kill()
        else:
            self.image = self.imageLst[self.frame]
            self.rect = self.image.get_rect(center=self.rect.center)

class sExplosion(Explosion):
    @staticmethod
    def init(screenWidth):
        size = int(screenWidth * 0.12)
        sExplosion.images = [pygame.transform.scale(\
                pygame.image.load('images/ship-explosions/'+str(i)+'.png'), \
                (size, size)) for i in range(1, 5)]

    def __init__(self, center):
        super(sExplosion, self).__init__(center, sExplosion.images)

class eExplosion(Explosion):
    @staticmethod
    def init(screenWidth):
        eExplosion.images = []
        size = int(screenWidth * 0.01)
        for img in os.listdir('images/enemy-explosions'):
            image = pygame.image.load('images/enemy-explosions/'+ str(img)).convert_alpha()
            w, h = image.get_size()
            image = pygame.transform.scale(image, (w+size, h+size))
            eExplosion.images.append(image)

    def __init__(self, center):
        super(eExplosion, self).__init__(center, eExplosion.images)
        self.frame_rate = 50 * 1.5
