import pygame
from Models import agent
from Models.reward import Reward
from Models.spot import Spot
from Models.agent import Agent
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


class World:

    def __init__(self,width,rows,n_agents,n_rewards) -> None:
        self.agents = []
        self.rewards = []
        self.width = width
        self.rows = rows
        self.cols = rows
        self.win  = pygame.display.set_mode((self.width, self.width))
        pygame.display.set_caption("Tri Collectif SMA - Khalid CHBAB - Adnane DRIOUCHE")
        self.n_rewards = n_rewards
        self.n_agents = n_agents
        self.terrain = None

    def world_populate(self,memory_size,k,k_n):
        self.agents, positions = self.__generate_agents(self.n_agents,memory_size,k,k_n)
        self.rewards = self.__generate_rewards(positions,self.n_rewards)
    

    def __get_start_place(self,l,rows):
        while True:
            t = (random.randrange(0,rows),random.randrange(0,rows))
            if t not in l:
                return t

    def __generate_agents(self,n,memory_size,k,k_n):
        l = []
        agents = []
        for i in range(n):
            row,col = self.__get_start_place(l,self.rows)
            agents.append(Agent("A"+str(i),row,col,self.width // self.rows,memory_size,k,k_n))
            l.append((row,col))
        return agents,l

    def __generate_rewards(self,l,n):
        rewards = []
        for i in range(n):
            row,col = self.__get_start_place(l,self.rows)
            rewards.append(Reward("A",row,col,self.width // self.rows))
            l.append((row,col))
            row,col = self.__get_start_place(l,self.rows)
            rewards.append(Reward("B",row,col,self.width // self.rows))
            l.append((row,col))
        return rewards

    def build_world(self):
        terrain = []
        gap = self.width // self.rows
        for i in range(self.rows):
            terrain.append([])
            for j in range(self.rows):
                spot = Spot(i, j, gap, self.rows)
                terrain[i].append(spot)

        self.terrain = terrain


    def draw_world(self):
        gap = self.width // self.rows
        for i in range(self.rows):
            pygame.draw.line(self.win, GREY, (0, i * gap), (self.width, i * gap))
            for j in range(self.rows):
                pygame.draw.line(self.win, GREY, (j * gap, 0), (j * gap, self.width))

    def draw(self):
        self.win.fill(WHITE)
        for row in self.terrain:
            for spot in row:
                spot.draw(self.win)
                spot.reset()
        for a in self.agents:
            self.terrain[a.row][a.col].agent = a
            a.draw(self.win)
        for r in self.rewards:
            if not r.is_taken:
                self.terrain[r.row][r.col].reward = r
                r.draw(self.win)
            else :
                self.terrain[r.row][r.col].reward = None

        self.draw_world()
        pygame.display.update()

    def __get_infos(self,a:Agent,grid):
        row = a.row
        col = a.col
        space = set()
        for i in range(-1,2):
            for j in range(-1,2):
                if i == 0 and j == 0:
                    space.add((0,0))
                else :
                    if row + i >= self.rows or col + j >= self.rows or row + i < 0 or col + j < 0:
                        space.add((0,0))
                    else :
                        space.add((i,j) if grid[row+i][col+j].is_empty() else (0,0))
        space.remove((0,0))
        return space,grid[row][col]
    
    def __get_infos_backup(self,a:Agent,grid):
        row = a.row
        col = a.col
        space = set()
        rewards = []
        for i in range(-1,2):
            for j in range(-1,2):
                if i == 0 and j == 0:
                    space.add((0,0))
                else :
                    if row + i >= self.rows or col + j >= self.rows or row + i < 0 or col + j < 0:
                        space.add((0,0))
                    else :
                        space.add((i,j) if grid[row+i][col+j].is_empty() else (0,0))
                        if grid[row+i][col+j].is_reward():
                            rewards.append((grid[row+i][col+j].reward,i,j))
        space.remove((0,0))
        return space,rewards


    def decision(self):
        for a in self.agents:
            posibilities,rewards = self.__get_infos(a,self.terrain)
            a.action(posibilities,rewards)

