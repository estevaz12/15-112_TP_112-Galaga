import pygame
from pygameGame import PygameGame

class Start(PygameGame):
    def init(self):
        self.logo = pygame.transform.scale(pygame.image.load('images/galaga-logo.png').convert_alpha(), \
                (int(self.height/2), int(self.width/2)))
        startFont = pygame.font.SysFont('emulogic', 15)
        self.startTxt = startFont.render("Press 'SPACE' to start.", False, \
                        (0,255,255))
        self.displayTxt = True
        self.time = 0

    def keyPressed(self, keyCode, mod):
        if keyCode == pygame.K_SPACE:
            self.state = 'game'

    def timerFired(self, dt):
        self.time += 1
        if self.time % 50 == 0: # every second
            self.displayTxt = not(self.displayTxt)

    def redrawAll(self, screen):
        w, h = self.logo.get_size()
        alignX = self.width/2 - w/2
        alignY = self.height/2 - h/2
        screen.blit(self.logo, (alignX, alignY))

        if self.displayTxt:
            w2, h2 = self.startTxt.get_size()
            alignX2 = (alignX + w/2) - w2/2
            alignY2 = (alignY + h + 10) - h2/2
            screen.blit(self.startTxt, (alignX2, alignY2))
