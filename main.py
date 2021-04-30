import pygame
from pygame.locals import *
pygame.init()

import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    # Set up the drawing window
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    theta = 0
    d_theta = 2*math.pi/5e3
    num_terms = 3
    fund_radius = 100

    plot_point_list = []

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill(BLACK)

        prev_dot_pos = (SCREEN_WIDTH/4, SCREEN_HEIGHT/2)
        for term in range(num_terms):
            n = term*2+1

            cntr_pos = prev_dot_pos
            radius = fund_radius/n
            width = 2
            pygame.draw.circle(screen, WHITE, cntr_pos, radius, width)

            dot_pos = (cntr_pos[0] + radius*math.cos(n*theta), cntr_pos[1] + radius*math.sin(n*theta))
            theta = theta + d_theta if theta < 2*math.pi else 0
            radius = 5
            pygame.draw.circle(screen, WHITE, dot_pos, radius)

            pygame.draw.line(screen, WHITE, cntr_pos, dot_pos)

            prev_dot_pos = dot_pos

        endpoint = prev_dot_pos

        plot_point_list = [(point[0]+0.1,point[1]) for point in plot_point_list]
        plot_point_list.append((3*SCREEN_WIDTH/5, endpoint[1]))
        if len(plot_point_list) > 2e3:
            plot_point_list.pop(0)
        if len(plot_point_list)>=2:
            pygame.draw.lines(screen, WHITE, False, plot_point_list, 2)       

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()