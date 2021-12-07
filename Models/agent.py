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
        self.stock_w= None
        self.k = k
        self.k_n = k_n

        # part 2
        self.waiting = False
        self.w_counting = 0
        self.detected_phero = 0

    def action(self,posibilities,spot,rewards,agents_asking):
        if self.waiting:
            self.w_counting = self.w_counting + 1 if self.w_counting <= 20 else 0
            if self.w_counting == 21:
                self.waiting = False
        else:
            self.__memory_control(posibilities,spot,rewards)
            for a in agents_asking:
                a.help()
            if self.detected_phero == 0:
                if self.stock is None:
                    for r in rewards:
                        result = self.__take(r)
                        if result == 1:
                            if r.type == "C":
                                self.send_phero_signal()
                                self.stock_w = r
                            else:
                                r.is_taken = True
                                self.stock = r
                            break
            if not self.waiting :
                self.move(posibilities)
                if self.stock:
                    result = self.__drop(self.stock)
                    if result == 1:
                        self.stock.is_taken = False
                        self.stock.change_pos(self.row,self.col)
                        self.stock = None

    # part 2

    def send_phero_signal(self):
        self.waiting = True


    def __memory_control(self,pos,spot,rewards):
        for r in rewards:
            if len(self.memory) == self.memory_size:
                self.memory.pop()
            self.memory.insert(0,r.type)
        for i in range(8-len(rewards)):
            self.memory.insert(0,0)

    def __calculate_f(self):
        fa = self.memory.count("A")
        fb = self.memory.count("B")
        fc = self.memory.count("C")

        return fa/len(self.memory),fb/len(self.memory),fc/len(self.memory)
    
    def __calculate_take(self,r):
        fa,fb,fc = self.__calculate_f()
        if r.type =="A":
            return (self.k/(self.k+fa))**2
        if r.type =="B":
            return (self.k/(self.k+fb))**2
        if r.type =="C":
            return (self.k/(self.k+fc))**2

    def __calculate_drop(self,r):
        fa,fb,fc = self.__calculate_f()
        if r.type =="A":
            return (self.k_n/(self.k_n+fa))**2
        if r.type =="B":
            return (self.k_n/(self.k_n+fb))**2
        if r.type =="C":
            return (self.k_n/(self.k_n+fc))**2
    
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
            row, col = self.move_to_phero(posibilities)
            # row, col = random.choice(list(posibilities))
            self.row = self.row + row
            self.col = self.col + col
            self.y = self.row * self.width
            self.x = self.col * self.width



    def move_to_phero(self,pos):
        max = 0
        max_i = 0
        max_j = 0
        for i,j,d in list(pos):
            if d > max:
                max= d
                max_i = i
                max_j = j
                self.detected_phero = 1
                self.coming_for_help = True
        if max == 0:
            self.detected_phero = 0
            s,j,r = random.choice(list(pos))
            self.coming_for_help = False
            return s,j
        else:
            return max_i,max_j

            
    def help(self):
        self.waiting = False
        self.w_counting = 0
        self.stock = self.stock_w
        self.stock_w = None
        self.stock.is_taken = True



    def draw(self, win):
            if not self.stock:
                rect = pygame.draw.rect(win, GREEN, (self.x, self.y, self.width, self.width))
            else:
                rect = pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.width))
            
    