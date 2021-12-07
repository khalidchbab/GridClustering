import pygame


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.y = row * width
        self.x = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.agent = None
        self.reward = None

        # part 2
        self.phero = 0
    
    def is_empty(self):
        return True if not self.agent else False
        # return True if not self.agent and not self.reward else False
        
    def get_pos(self):
        return self.row, self.col
    
    def is_reward(self):
        return True if not self.agent and self.reward else False
    
    def reset(self):
        self.agent = None
        self.reward = None


    def draw(self, win):
        if self.phero != 0:
            self.phero = self.phero - 5 if self.phero - 3 > 0 else 0
        self.color = WHITE if self.phero == 0 else (255 - self.phero, 255 - self.phero, 255 - self.phero)
        if self.is_empty():
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
