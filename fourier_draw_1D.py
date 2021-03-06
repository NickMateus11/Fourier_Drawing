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
    d_theta = 2*math.pi/2e3
    dt = 0.1
    fund_radius = SCREEN_HEIGHT/5

    with open('drawing.xy','r') as file:
        draw_points = [tuple([int(float(n)) for n in p.split(',')]) for p in file.read().strip().split()]
    
    y_t = [p[1] for p in draw_points]
    dft_y = np.fft.rfft(y_t)
    dft_y *= fund_radius/np.linalg.norm(dft_y)

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

        prev_dot_pos = (SCREEN_WIDTH/4, SCREEN_HEIGHT/2)
        for i in range(len(dft_y)):
            mag = math.sqrt((dft_y[i].real)**2 + (dft_y[i].imag)**2)
            phase = math.atan2(dft_y[i].imag,dft_y[i].real)
            # circle
            cntr_pos = prev_dot_pos
            radius = mag
            width = 2
            pygame.draw.circle(screen, WHITE, cntr_pos, radius, width)

            # dot on outer edge
            dot_pos = (cntr_pos[0] + radius*math.cos(i*theta+phase), cntr_pos[1] + radius*math.sin(i*theta+phase))
            radius = 5
            pygame.draw.circle(screen, WHITE, dot_pos, radius)

            # line from center to outer dot
            pygame.draw.line(screen, WHITE, cntr_pos, dot_pos)

            prev_dot_pos = dot_pos
        
        # update angle step
        theta = theta + d_theta if theta < 2*math.pi else 0
        endpoint = prev_dot_pos

        # move all points to the right by step amount
        plot_point_list = [ (point[0] + dt, point[1]) for point in plot_point_list]
        plot_point_list.append((3*SCREEN_WIDTH/5, endpoint[1]))

        # remove off-screen points
        if len(plot_point_list) > 2e3:
            plot_point_list.pop(0)

        # draw line from last circle to plot
        pygame.draw.line(screen, WHITE, endpoint, plot_point_list[-1])

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