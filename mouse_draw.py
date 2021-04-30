import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    # Set up the drawing window
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    points = []
    draw = False

    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                with open('drawing.xy','w') as file:
                    file.writelines([f'{p[0]},{p[1]}\n' for p in points])
                    print("saved!")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                with open('drawing.xy','r') as file:
                    points = [tuple([int(x) for x in p.split(',')]) for p in file.read().strip().split()]
                    print("loaded!")

        # Fill the background with black
        screen.fill(BLACK)

        # collect points if mouse down
        if pygame.mouse.get_pressed()[0]:
            if not draw:
                points = []
            draw = True
            pos_tuple = pygame.mouse.get_pos()
            if not points or not points[-1] == pos_tuple:
                points.append(pos_tuple)
        else: 
            draw = False
        
        # draw points
        if len(points) > 2:
            pygame.draw.lines(screen, WHITE, False, points, width=2)

        # update screen
        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    main()