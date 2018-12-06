# Everything that has to do with name entering and the scoreboard

import pygame
import string
from pygameGame import PygameGame

class ScoreBoard(PygameGame):
    def init(self):
        self.screen = "name"

        self.name = ""
        self.nameFont = pygame.font.SysFont('emulogic', 30)
        self.nameTxt = self.nameFont.render(self.name, False, (0, 255, 255))

        initialsF = pygame.font.SysFont('emulogic', 20)
        self.initials = initialsF.render("Enter initials", False, (255, 255, 255))

        self.display = False
        self.time = 0

        selectF = pygame.font.SysFont('emulogic', 15)
        self.enter = selectF.render("Press 'Enter' to continue", False, (255, 0, 0))

        self.scores = {}
        self.scoresFont = pygame.font.SysFont('emulogic', 15)

    # From: https://stackoverflow.com/questions/4706499/how-do-you-append-to-a-file
    @staticmethod
    def appendText(path, contents):
        with open(path, "a") as f:
            f.write(contents)

    # From: https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    @staticmethod
    def readFile(path):
        with open(path, "rt") as f:
            return f.read()

    def keyPressed(self, keyCode, mod):
        if self.screen == "name":
            if  len(self.name) < 3 and keyCode in range(pygame.K_a, pygame.K_z + 1):
                letter = pygame.key.name(keyCode)
                self.name += letter

            if len(self.name) > 0 and keyCode == pygame.K_BACKSPACE:
                self.name = self.name[:-1]

            if len(self.name) == 3 and keyCode == pygame.K_RETURN:
                result = self.name + "\t" + str(self.timePlaying) + "\n"
                ScoreBoard.appendText("scores-"+self.difficulty+".txt", result)
                self.screen = "board"

    def timerFired(self, dt):
        self.time += 1
        if self.screen == "name":
            self.nameTxt = self.nameFont.render(self.name, False, (0, 255, 255))
        elif self.screen == "board":
            file = ScoreBoard.readFile("scores-"+self.difficulty+".txt")
            for line in file.splitlines():
                result = line.split("\t")
                self.scores[float(result[1])] = result[0]

        if self.time % 35 == 0:
            self.display = not(self.display)

    def redrawAll(self, screen):
        if self.screen == "name":
            w, h = self.initials.get_size()
            alignX = self.width/2 - w/2
            alignY = self.margin - h/2
            screen.blit(self.initials, (alignX, alignY))

            w, h = self.nameTxt.get_size()
            alignX = self.width/2 - w/2
            alignY = self.height/2 - h/2
            screen.blit(self.nameTxt, (alignX, alignY))

            if self.display:
                pygame.draw.rect(screen, (255, 255, 255), (alignX+w, alignY, 30, 38))

            w, h = self.enter.get_size()
            alignX = self.width/2 - w/2
            alignY = self.height - self.margin - h/2
            screen.blit(self.enter, (alignX, alignY))

        elif self.screen == "board":
            txt = self.scoresFont.render('Times', False, (255,0,0))
            w, h = txt.get_size()
            alignX = self.width/2 - w/2
            alignY = self.margin - h/2
            screen.blit(txt, (alignX, alignY))

            times = sorted(list(self.scores))
            results = []
            for t in times:
                results.append(self.scores[t] + "\t" + str(t) + " s")

            if len(results) > 10:
                for i in range(10):
                    currScore = self.scoresFont.render(results[i], False, (255,255,255))
                    w, h = currScore.get_size()
                    alignX = self.width/3
                    alignY = self.height/6 + ((h + 15) * i)
                    screen.blit(currScore, (alignX, alignY))
            else:
                for i in range(len(results)):
                    currScore = self.scoresFont.render(results[i], False, (255,255,255))
                    w, h = currScore.get_size()
                    alignX = self.width/3
                    alignY = self.height/6 + ((h + 15) * i)
                    screen.blit(currScore, (alignX, alignY))

            if self.display:
                txt = self.scoresFont.render("Press 'R' to restart", False, (0,255,255))
                w, h = txt.get_size()
                alignX = self.width/2 - w/2
                alignY = self.height - self.margin - h/2
                screen.blit(txt, (alignX, alignY))
