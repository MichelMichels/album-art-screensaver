#!/usr/bin/python
#
# pygame version

#debug
import time
import os, signal

import sys, pygame
from random import randint

# colors
white = 255, 240, 200
black = 20, 20, 20

# window size
window_height = 480
window_width = 640

# cover width and height
space_width_height = 200

# wait time
wait_time = 2000

# set num col and row
if window_height % space_width_height > 0:
    num_row_spaces = int(window_height / space_width_height) + 1
else:
    num_row_spaces = int(window_height / space_width_height)

if window_width % space_width_height > 0:
    num_col_spaces = int(window_width / space_width_height) + 1
else:
    num_col_spaces = int(window_width / space_width_height)

covers = []
cover_spaces = []

class CoverSpace(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.pos = (x , y)
        self.width = width
        self.height = height
        self.current_cover = None

    def get_rect(self):
        return pygame.Rect((self.x, self.y), (self.width, self.height))

    def get_size(self):
        return (self.width, self.height)

class Cover(object):
    def __init__(self, image):
        self.image = image

def initialise(screen, background):
    # load coverspaces
    for row in range(num_row_spaces):
        for col in range(num_col_spaces):
            cover_spaces.append(CoverSpace(col * space_width_height, row * space_width_height, space_width_height, space_width_height))

    # load covers
    with open('cover_path.txt') as f:
        for line in f:
            try:
                # add cover to covers list
                covers.append(Cover(pygame.image.load(line.rstrip() + '/cover.jpg').convert()))

                # fill screen for the first time
                found_empty_space = False
                while found_empty_space == False :
                    num_empty_spaces = 0
                    for space in cover_spaces:
                        if space.current_cover == None:
                            num_empty_spaces = num_empty_spaces + 1
                    if num_empty_spaces == 0:
                        break

                    random_space = cover_spaces[randint(0, len(cover_spaces) - 1)]
                    if random_space.current_cover == None:
                        last_cover = covers[-1]
                        scaled_cover = pygame.transform.scale(last_cover.image, random_space.get_size())
                        random_space.current_cover = last_cover

                        # draw on screen
                        screen.blit(background, random_space.pos, random_space.get_rect())
                        screen.blit(scaled_cover, random_space.pos)
                        pygame.display.update(random_space.get_rect())

                        found_empty_space = True
            except pygame.error:
                pass
def animate(screen, background):
    # change one coverspace
    random_space = cover_spaces[randint(0, len(cover_spaces) - 1)]
    random_cover = covers[randint(0, len(covers) - 1)]

    # closing animation
    if random_space.current_cover != None:
        for i in range(int(space_width_height / 10) + 1):
            scaled_current_cover = pygame.transform.scale(random_space.current_cover.image, (random_space.width - 10*i, random_space.height))
            screen.blit(background, random_space.pos, random_space.get_rect())
            screen.blit(scaled_current_cover, (random_space.x + 5*i, random_space.y))
            pygame.display.update(random_space.get_rect())
            pygame.time.delay(10)

    # opening animation
    for i in range(int(space_width_height / 10) + 1):
        scaled_random_cover = pygame.transform.scale(random_cover.image, (10*i, random_space.height))
        screen.blit(background, random_space.pos, random_space.get_rect())
        screen.blit(scaled_random_cover, (random_space.x + int(random_space.width / 2) - 5*i, random_space.y))
        pygame.display.update(random_space.get_rect())
        pygame.time.delay(10)

def main():
    # debug
    print("Number of rows: ", num_row_spaces)
    print("Number of cols: ", num_col_spaces)

    # init and prepare screen
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    #pygame.display.toggle_fullscreen()

    background = pygame.Surface(screen.get_size())
    background.fill(black)

    initialise(screen, background)

    pygame.display.set_caption('Album art cover screensaver by Michel Michels')
    pygame.display.update()

    # ms between animations
    animate_event = pygame.USEREVENT
    pygame.time.set_timer(animate_event, 1000)

    while True:
        if pygame.event.get(pygame.QUIT): break
        if pygame.event.get(pygame.KEYDOWN): break

        for event in pygame.event.get():
            if event.type == animate_event:
                animate(screen, background)
                # reset event
                pygame.time.set_timer(animate_event, randint(2,5)*1000)

    pygame.quit()
    sys.exit()


# if python says run, then we should run
if __name__ == '__main__':
    main()
