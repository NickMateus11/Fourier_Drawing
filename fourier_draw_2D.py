import pygame
from pygame.locals import *

import math
import argparse
import numpy as np


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def main(args):
    # Set up the drawing window
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    font = pygame.font.SysFont('Times New Roman', 20)

    NUM_TERMS = args.terms

    theta = 0
    d_theta = 2*math.pi/5e3
    dt = 0.1
    fund_radius = SCREEN_HEIGHT/5

    # load drawing
    with open('drawing.xy','r') as file:
        draw_points = [tuple([int(n) for n in p.split(',')]) for p in file.read().strip().split()]

    # structure data as required
    c, s = np.cos(-math.pi/4), np.sin(-math.pi/4)
    R = np.array(((c, -s), (s, c)))
    draw_points = np.matmul(R, np.array(draw_points).T).T
    draw_points = np.concatenate((draw_points, draw_points[::-1]))   # make the points symmetric

    dft2 = np.fft.rfft2(draw_points)[:NUM_TERMS]
    print(np.linalg.norm(dft2))
    dft2 *= 500 / np.linalg.norm(dft2) 

    # extract mag and phase of each frequency
    dft_y = [[math.sqrt((y.real)**2 + (y.imag)**2), math.atan2(y.imag,y.real), i] for i,y in enumerate(dft2[:,0])]
    dft_x = [[math.sqrt((x.real)**2 + (x.imag)**2), math.atan2(x.imag,x.real), i] for i,x in enumerate(dft2[:,1])]

    # sort by mag
    # dft_y = sorted(dft_y, key=lambda k: k[2])
    # dft_x = sorted(dft_x, key=lambda k: k[2])

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
        for e in range(1,len(dft2)):
            mag = dft_y[e][0]
            phase = dft_y[e][1] + math.pi/2
            i = dft_y[e][2]
            # circle - left
            cntr_pos1 = prev_dot_pos1
            radius = mag
            width = 1
            pygame.draw.circle(screen, WHITE, cntr_pos1, radius, width)

            # dot on outer edge
            dot_pos1 = (cntr_pos1[0] + radius*math.cos(i*theta+phase), cntr_pos1[1] + radius*math.sin(i*theta+phase))
            # radius = 5
            # pygame.draw.circle(screen, WHITE, dot_pos1, radius)

            # line from center to outer dot
            pygame.draw.line(screen, WHITE, cntr_pos1, dot_pos1)
            
            # ----
            mag = dft_x[i][0]
            phase = dft_x[i][1]
            i = dft_x[e][2]
            # circle - top
            cntr_pos2 = prev_dot_pos2
            radius = mag
            width = 1
            pygame.draw.circle(screen, WHITE, cntr_pos2, radius, width)
            # dot on outer edge
            dot_pos2 = (cntr_pos2[0] + radius*math.cos(i*theta+phase), cntr_pos2[1] + radius*math.sin(i*theta+phase))
            # radius = 5
            # pygame.draw.circle(screen, WHITE, dot_pos2, radius)
            # line from center to outer dot
            pygame.draw.line(screen, WHITE, cntr_pos2, dot_pos2)

            prev_dot_pos1 = dot_pos1
            prev_dot_pos2 = dot_pos2
        
        # update angle step
        theta = theta + d_theta if theta < 2*math.pi else 0
        endpoint1 = prev_dot_pos1
        endpoint2 = prev_dot_pos2

        # remove points as list grows
        if len(plot_point_list) > 2.5e3:
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
    parser.add_argument("-t", "--terms", help="number of sinusoidal terms", type=int, default=50)
    args = parser.parse_args()

    main(args)