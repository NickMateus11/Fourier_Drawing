import pygame
import argparse as ap
import sys
from time import sleep
from cmath import *

def round(p):
    x, y = p
    return (int(x), int(y))

p = ap.ArgumentParser(description = "Replicate drawing using Fourier Transform")
p.add_argument("-n", default = 50, type = int, help = "number of circles to use (default is 10)")
p.add_argument("-m", "--mode", default = "loop", choices = ["loop", "increase"], help = "whether the number of circles should stay constant or increase after each loop (default is 'loop')")
p.add_argument("-d", "--decay", default = 0.6, type = float, help = "from 0 to 1, how strongly should the track brightness decay (default is 0.6)")
p.add_argument("-t", "--trace", action="store_true", help = "if set the original handdrawn trace will be left visible while the program replicates it")
args = p.parse_args()

decay = max(0, min(1, args.decay))

w, h = 800, 600

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((w, h))

white = pygame.Color(255, 255, 255)
yellow = pygame.Color(255, 255, 0)
grey = pygame.Color(120, 120, 120)
dark_grey = pygame.Color(90, 90, 90)
black = pygame.Color(0,0,0)

font = pygame.font.SysFont(pygame.font.get_default_font(), 30)

draw = False
track = []

print("recording track")

wait = True
while wait:
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE or e.type == pygame.QUIT:
            sys.exit()

    if pygame.mouse.get_pressed()[0]:
        if not draw:
            track = []
        draw = True
        pos_tuple = pygame.mouse.get_pos()
        if not track or not track[-1] == pos_tuple:
            track.append(pos_tuple)
    elif draw:
        wait = False
        
    
    # draw points
    if len(track) > 2:
        pygame.draw.lines(screen, white, False, track, width=2)

    for p in track:
        screen.set_at(round(p), white)
    pygame.display.update()

print("processing track")

if ((track[0][0] - track[-1][0])**2 + (track[0][1] - track[-1][1])**2)**0.5 > min(w,h)/2:
    track = track + track[::-1]
tl = len(track)
for i in range(tl):
    x, y = track[i]
    track[i] = (x-w//2, y-h//2)


ftrack = []
n = args.n
while True:
    print("drawing with n = %d"%n)
    if ftrack == []:
        c = []
        for i in range(n, -n-1, -1):
            c.append(sum(exp(2*pi*1j*i*t/tl)*(track[t][0]+track[t][1]*1j) for t in range(tl))/tl)

    for t in range(tl):
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE or e.type == pygame.QUIT:
                sys.exit()
        sleep(0.05)
        screen.fill(black)
        z = w//2 + h//2*1j
        # for i in range(2*n+1):
        for i in sum(zip(range(n+1, 2*n+1), range(n-1, -1, -1)), (n,)):
            old_z = z
            z += exp(2*pi*1j*(i-n)*t/tl)*c[i] 
            pygame.draw.line(screen, grey, (old_z.real, old_z.imag), (z.real, z.imag))
            r = ((old_z.real - z.real)**2 + (old_z.imag - z.imag)**2)**0.5
            if r > 1:
                pygame.draw.circle(screen, grey, (old_z.real, old_z.imag), r, 1)
        if len(ftrack) < tl:
            ftrack.append(z)

        #z = sum(exp(2*pi*1j*(i-n)*t/tl)*c[i] for i in range(2*n+1))
        if args.trace:
            for p in track:
                screen.set_at(round((p[0]+w//2, p[1]+h//2)), black)
        points = [(p.real, p.imag) for p in ftrack]

        if len(points)>2:
            pygame.draw.lines(screen, white, False, points,2)
        pygame.display.update()

    if args.mode == "increase":
        n += 1
        ftrack = []
