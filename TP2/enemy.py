from gameObject import GameObject

class Enemy(GameObject):
    speed = 8
    def __init__(self, x, y, image, size):
        super(Enemy, self).__init__(x, y, image, size)
        self.diving = False


    def dive(self):
        self.diving = True

    def update(self, )
