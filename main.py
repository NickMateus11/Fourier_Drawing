import pygame
from pygame.locals import *

import math
import argparse


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def dft(f_n, n):
    x_n = [p[0] for p in f_n]
    y_n = [p[1] for p in f_n]
    a_k = (2/len(x_n))*sum([x_n[t]*math.cos(n*t/len(x_n)) for t in range(len(x_n))])
    b_k = (2/len(y_n))*sum([y_n[t]*math.sin(n*t/len(y_n)) for t in range(len(y_n))])
    return a_k, b_k

def main(args):
    # Set up the drawing window
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    font = pygame.font.SysFont('Times New Roman', 20)

    NUM_TERMS = args.terms

    theta = 0
    d_theta = 2*math.pi/2e3
    dt = 0.1
    fund_radius = SCREEN_HEIGHT/5

    with open('drawing.xy','r') as file:
        draw_points = [tuple([int(x) for x in p.split(',')]) for p in file.read().strip().split()]
    plot_point_list = []

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with black
        screen.fill(BLACK)

        prev_dot_pos1 = (SCREEN_WIDTH/5, 7*SCREEN_HEIGHT/10)
        prev_dot_pos2 = (7*SCREEN_WIDTH/10, SCREEN_HEIGHT/5)
        for term in range(NUM_TERMS):
            n = term*2+1
            [a_n, b_n] = dft(draw_points, n)
            # circle - left
            cntr_pos1 = prev_dot_pos1
            radius = fund_radius * a_n
            width = 2
            pygame.draw.circle(screen, WHITE, cntr_pos1, abs(radius), width)
            # dot on outer edge
            dot_pos1 = (cntr_pos1[0] + radius*math.cos(n*theta), cntr_pos1[1] + radius*math.sin(n*theta))
            radius = 5
            pygame.draw.circle(screen, WHITE, dot_pos1, radius)
            # line from center to outer dot
            pygame.draw.line(screen, WHITE, cntr_pos1, dot_pos1)

            # circle - top
            cntr_pos2 = prev_dot_pos2
            radius = fund_radius * b_n
            width = 2
            pygame.draw.circle(screen, WHITE, cntr_pos2, abs(radius), width)
            # dot on outer edge
            dot_pos2 = (cntr_pos2[0] + radius*math.cos(n*theta), cntr_pos2[1] + radius*math.sin(n*theta))
            radius = 5
            pygame.draw.circle(screen, WHITE, dot_pos2, radius)
            # line from center to outer dot
            pygame.draw.line(screen, WHITE, cntr_pos2, dot_pos2)

            prev_dot_pos1 = dot_pos1
            prev_dot_pos2 = dot_pos2
        
        # update angle step
        theta = theta + d_theta if theta < 2*math.pi else 0
        endpoint1 = prev_dot_pos1
        endpoint2 = prev_dot_pos2

        # remove points as list grows
        if len(plot_point_list) > 2e3:
            plot_point_list.pop(0)

        # draw line from last circle to plot
        draw_point = (endpoint2[0], endpoint1[1])
        pygame.draw.line(screen, WHITE, endpoint1, draw_point)
        pygame.draw.line(screen, WHITE, endpoint2, draw_point)
        pygame.draw.circle(screen, WHITE, draw_point, 5)

        # add meeting point to point list
        plot_point_list.append(draw_point)

        # draw lines connecting plot points
        if len(plot_point_list)>=2:
            pygame.draw.lines(screen, WHITE, False, plot_point_list, 2)       

        # display text and update screen
        textsurface = font.render(f"Terms: {NUM_TERMS}", True, WHITE)
        screen.blit(textsurface, (SCREEN_WIDTH/5, SCREEN_HEIGHT/10))
        pygame.display.flip()


    pygame.quit()

if __name__ == '__main__':
    # get args
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--terms", help="number of sinusoidal terms", type=int, default=3)
    args = parser.parse_args()

    main(args)