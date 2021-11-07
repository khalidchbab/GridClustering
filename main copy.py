import pygame
from Models import agent
from Models.reward import Reward
from Models.spot import Spot
from Models.agent import Agent
import time
import copy
import random


WIDTH = 800
ROWS = 50


RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

def get_start_place(l,s):
    while True:
        t = (random.randrange(0,s),random.randrange(0,s))
        if t not in l:
            return t

def generate_agents(n,s,w):
    l = []
    agents = []
    for i in range(n):
        row,col = get_start_place(l,s)
        agents.append(Agent("A"+str(i),row,col,w // s,8,0.1,0.3))
        l.append((row,col))
    return agents,l

def generate_rewards(l,n,s,w):
    rewards = []
    for i in range(n):
        row,col = get_start_place(l,s)
        rewards.append(Reward("A",row,col,w // s))
        l.append((row,col))
        row,col = get_start_place(l,s)
        rewards.append(Reward("B",row,col,w // s))
        l.append((row,col))
    return rewards

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, agents, rewards, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.reset()
    for a in agents:
        grid[a.row][a.col].agent = a
        a.draw(win)
    for r in rewards:
        if not r.is_taken:
            grid[r.row][r.col].reward = r
            r.draw(win)
        else :
            grid[r.row][r.col].reward = None

    draw_grid(win, rows, width)
    pygame.display.update()

def get_infos(a:Agent,grid):
    row = a.row
    col = a.col
    surrounding = [[],[],[]]
        # print(f"row : {row} and col {col}")
        # for i in range(-1,2):
        #     for j in range(-1,2):
        #         if i == 0 and j == 0:
        #             space[i].append((0,0))
        #         else :
        #             if row + i >= ROWS or col + j >= ROWS or row + i < 0 or col + j < 0:
        #                 space[i].append((0,0))
        #             else :
        #                 print(f"row : {row} and col {col} and i {i} and j {j}")
        #                 space[i].append((i,j) if grid[row+1][col-1].is_empty() else (0,0))
    space = set()
    rewards = []
    for i in range(-1,2):
        for j in range(-1,2):
            if i == 0 and j == 0:
                space.add((0,0))
            else :
                if row + i >= ROWS or col + j >= ROWS or row + i < 0 or col + j < 0:
                    space.add((0,0))
                else :
                    space.add((i,j) if grid[row+i][col+j].is_empty() else (0,0))
                    if grid[row+i][col+j].is_reward():
                        rewards.append((grid[row+i][col+j].reward,i,j))
    space.remove((0,0))
    return space,rewards

def decision(win,grid,agents):
    for a in agents:
        # grid[a.row][a.col].agent = None
        posibilities,rewards = get_infos(a,grid)
        a.action(posibilities,rewards)
        # grid[a.row][a.col].agent = a


def main(win, width,n_agent,n_rewards,rows):
    ROWS = rows
    grid = make_grid(ROWS, width)
    agents,positions = generate_agents(n_agent,ROWS,width)
    rewards = generate_rewards(positions,n_rewards,ROWS,width)
    run = True
    paused = False
    i = 0
    while run:
        if not paused:
            decision(win,grid,agents)
            draw(win, grid, agents,rewards, ROWS, width)
            print(f"round {i}")
            i = i + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
        # time.sleep(0)
            
    pygame.quit()

main(WIN, WIDTH,20,100,50)