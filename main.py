import pygame
import time
from Models.world import World
from Models.reward import Reward

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(width,n_agent,n_rewards,rows,memory_size,k,k_n):
    world = World(width,rows,n_agent,n_rewards)
    world.build_world()
    world.world_populate(memory_size,k,k_n)
    run = True
    paused = False
    i = 0
    while run:
        if not paused:
            world.decision()
            world.draw()
            print(f"Iteration : {i}")
            i = i + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
        time.sleep(0)
            
    pygame.quit()

main(800,20,200,50,10,0.1,0.3)

