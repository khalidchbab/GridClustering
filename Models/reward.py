from random import randrange
import pygame
import random

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

class Reward:
    
    def __init__(self,type,row,col,width) -> None:
        self.type = type
        self.row = row
        self.col = col
        self.y = row * width
        self.x = col * width
        self.width = width
        self.is_taken = False
    
    def change_pos(self,row,col):
        self.row = row
        self.col = col
        self.y = row * self.width
        self.x = col * self.width

    
    def draw(self, win):
        if self.type == "A" and not self.is_taken:
            cerc = pygame.draw.circle(win, PURPLE, (self.x + int(self.width/2), self.y+ int(self.width/2)),(self.width / 2)-4)
        if self.type == "B" and not self.is_taken:
            cerc = pygame.draw.circle(win, RED, (self.x + int(self.width/2), self.y+ int(self.width/2)),(self.width / 2)-4)
    
