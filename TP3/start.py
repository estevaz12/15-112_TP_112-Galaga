import pygame
from pygameGame import PygameGame

class Start(PygameGame):
    def init(self):
        self.logo = pygame.transform.scale(pygame.image.load('images/galaga-logo.png').convert_alpha(), \
                (int(self.height/2), int(self.width/2)))

        startFont = pygame.font.SysFont('emulogic', 15)
        self.diffTxt = startFont.render("Select difficulty:", False, \
                        (0,255,255))
        self.easy = startFont.render("Easy", False, \
                        (255,255,0))
        self.normal = startFont.render("Normal", False, \
                        (194,14,213))
        self.hard = startFont.render("Hard", False, \
                        (255,0,0))
        self.select = startFont.render("Press 'Space' to select", False, \
                        (6,229,20))
        self.selectSound = pygame.mixer.Sound('sounds/choose-mode.ogg')

        # Align logo
        w, h = self.logo.get_size()
        self.alignX = self.width/2 - w/2
        self.alignY = self.height/4 - h/2
        # Align difficulty select
        w2, h2 = self.diffTxt.get_size()
        self.alignX2 = (self.alignX + w/2) - w2/2
        self.alignY2 = (self.alignY + h + 30) - h2/2
        # Align 'easy'
        w3, h3 = self.easy.get_size()
        self.alignX3 = (self.alignX2 + w2/2) - w3/2
        self.alignY3 = (self.alignY2 + h2 + 30) - h3/2
        # Align 'normal'
        w4, h4 = self.normal.get_size()
        self.alignX4 = (self.alignX3 + w3/2) - w4/2
        self.alignY4 = (self.alignY3 + h3 + 20) - h4/2
        # Align 'hard'
        w5, h5 = self.hard.get_size()
        self.alignX5 = (self.alignX4 + w4/2) - w5/2
        self.alignY5 = (self.alignY4 + h4 + 20) - h5/2
        # Align 'select'
        w6, h6 = self.hard.get_size()
        self.alignX6 = w6/2
        self.alignY6 = (self.alignY5 + h5 + 30) - h6/2

        self.cursor = pygame.transform.rotate(pygame.transform.scale(\
                          pygame.image.load('images/ship-lives.png').convert_alpha(),\
                                           (15, 15)), 270)
        self.wC, hC = self.cursor.get_size()


        self.cX = self.alignX3 - self.wC - 10
        self.cY = self.alignY3

        self.mode = 0

        self.displayC = True
        self.time = 0

        self.difficulty = None
        self.soundTimer = 1.5
        self.playedSound = False

    def keyPressed(self, keyCode, mod):
        if keyCode == pygame.K_SPACE:
            self.selectSound.play()
            self.playedSound = True
            self.displayC = True

            if self.mode == 0:
                self.difficulty = 'easy'
            elif self.mode == 1:
                self.difficulty = 'normal'
            elif self.mode == 2:
                self.difficulty = 'hard'
        elif keyCode == pygame.K_DOWN:
            self.mode = (self.mode + 1) % 3
            if self.mode == 0:
                self.cX = self.alignX3 - self.wC - 10
                self.cY = self.alignY3
            elif self.mode == 1:
                self.cX = self.alignX4 - self.wC - 10
                self.cY = self.alignY4
            elif self.mode == 2:
                self.cX = self.alignX5 - self.wC - 10
                self.cY = self.alignY5
        elif keyCode == pygame.K_UP:
            self.mode = (self.mode - 1) % 3
            if self.mode == 0:
                self.cX = self.alignX3 - self.wC - 10
                self.cY = self.alignY3
            elif self.mode == 1:
                self.cX = self.alignX4 - self.wC - 10
                self.cY = self.alignY4
            elif self.mode == 2:
                self.cX = self.alignX5 - self.wC - 10
                self.cY = self.alignY5

    def timerFired(self, dt):
        self.time += 1
        if self.playedSound == False and self.time % 25 == 0: # every second
            self.displayC = not(self.displayC)

        if self.playedSound and self.time % 50 == 0:
            self.soundTimer -= 1

        if self.soundTimer <= 0:
            self.state = 'game'
            self.playedSound = False
            self.soundTimer = 1.5

    def redrawAll(self, screen):
        screen.blit(self.logo, (self.alignX, self.alignY))
        screen.blit(self.diffTxt, (self.alignX2, self.alignY2))
        screen.blit(self.easy, (self.alignX3, self.alignY3))
        screen.blit(self.normal, (self.alignX4, self.alignY4))
        screen.blit(self.hard, (self.alignX5, self.alignY5))
        if self.displayC:
            screen.blit(self.cursor, (self.cX, self.cY))
        screen.blit(self.select, (self.alignX6, self.alignY6))
