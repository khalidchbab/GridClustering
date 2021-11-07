from random import randrange
import pygame
import random
import numpy as np



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


class Agent:

    def __init__(self,name,row,col,width,memory_size,k,k_n) -> None:
        self.name = name
        self.row = row
        self.col = col
        self.y = row * width
        self.x = col * width
        self.width = width
        self.memory = []
        self.memory_size = memory_size
        self.stock = None
        self.k = k
        self.k_n = k_n

    def action(self,posibilities,spot):
        self.__memory_control(posibilities,spot)
        if self.stock is None:
            if not (spot.reward is None):
                r = spot.reward
                result = self.__take(r)
                if result == 1:
                    r.is_taken = True
                    self.stock = r
        self.move(posibilities)
        if self.stock:
            result = self.__drop(self.stock)
            if result == 1:
                self.stock.is_taken = False
                self.stock.change_pos(self.row,self.col)
                self.stock = None


    def __memory_control(self,pos,spot):
        if len(self.memory) == self.memory_size:
            self.memory.pop()
        tmp = spot.reward.type if spot.reward is not None else 0
        self.memory.insert(0,tmp)

    def __calculate_f(self):
        fa = self.memory.count("A")
        fb = self.memory.count("B")

        return fa/len(self.memory),fb/len(self.memory)
    
    def __calculate_take(self,r):
        fa,fb = self.__calculate_f()
        if r.type =="A":
            return (self.k/(self.k+fa))**2
        if r.type =="B":
            return (self.k/(self.k+fb))**2

    def __calculate_drop(self,r):
        fa,fb = self.__calculate_f()
        if r.type =="A":
            return (self.k_n/(self.k_n+fa))**2
        if r.type =="B":
            return (self.k_n/(self.k_n+fb))**2
    
    def __take(self,r):
        p = self.__calculate_take(r)
        take = np.random.choice(np.array([1,0]), p=[p,1-p])
        return True if take == 1 else False
    
    def __drop(self,r):
        p = self.__calculate_drop(r)
        take = np.random.choice(np.array([1,0]), p=[p,1-p])
        return True if take == 1 else False
        
    def move(self,posibilities):
        if len(posibilities) != 0:
            row, col = random.choice(list(posibilities))
            self.row = self.row + row
            self.col = self.col + col
            self.y = self.row * self.width
            self.x = self.col * self.width

    def draw(self, win):
            if not self.stock:
                rect = pygame.draw.rect(win, GREEN, (self.x, self.y, self.width, self.width))
            else:
                rect = pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.width))
            
    