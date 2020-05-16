import pygame
from pygame.locals import *
import time
import os
from dependencies.files import textbox
import json
import base64
from Tkinter import *
import tkMessageBox
import tkFileDialog
import win32gui, win32api, win32con

Title = "test"
quiz = None

PLAYERSSCORE = {} #""""dictionary, saves the points of each player"""
FONT_LIB = pygame.font.match_font('bitstreamverasans')[0:-10] + "\\" #finds the fony libary path
IMAGES_DIR = os.getcwd() + "\\images\\" #saves the path to the images libary
OST_DIR = os.getcwd() + "\\audio\\"
users = None
TotalQN = None

"""defauly pygame settings"""
MouseButtonDown = 6
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
TCHELET = (150, 150, 255)
MouseMotion = 4

#screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)  # full screen
screen = pygame.display.set_mode((800, 600))  # set screen wid =800, hieght =600

"""height and width of the screen"""
size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
WIDTH = size[0]
HEIGHT = size[1]
clock = pygame.time.Clock()

"""vars for un used libary update_login"""
LASTUPDATECALL = time.time()
NAMELIST = []
RANDO = 1

"""white surface in the size of the screen"""
BLACKSURFACE = pygame.Surface((WIDTH, HEIGHT))
BLACKSURFACE.fill(WHITE)


def main():
    pygame.display.set_caption("Kaboot")
    pygame.display.flip()
    pygame.font.init()

    a = textbox.OutputBox(screen, "Kaboot!", (WIDTH, int(100/600.*HEIGHT)), (0, int(50/600.*HEIGHT)), (255, 255, 255), 0, (), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf")
    Play = textbox.ButtonBox(screen, "Play!", (int((770-25)/800.*WIDTH)/2, int(580/600.*HEIGHT-490/600.*HEIGHT)), (int(25/800.*WIDTH), int(490/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf")
    Edit = textbox.ButtonBox(screen, "Edit...", (int((770-25)/800.*WIDTH)/2, int(580/600.*HEIGHT-490/600.*HEIGHT)), (int(800-25/800.*WIDTH) - int((770-25)/800.*WIDTH)/2, int(490/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf")

    onlyfiles = [f for f in os.listdir("dependencies\\quizes") if os.path.isfile(os.path.join("dependencies\\quizes", f))]
    onlyfiles = sorted(onlyfiles)
    print onlyfiles
    quizes = []
    n = 0
    counter = 0
    for file in onlyfiles[n:n+5]:
        if n < 0:
            n = len(onlyfiles) - 1
        quizes.append(textbox.ButtonBox(screen, file.split(".json")[0], (int(2*WIDTH/3), int(50/600.*HEIGHT)), (int(75/800.*WIDTH), int((200+55*counter)/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf"))
        counter += 1

    up = textbox.ButtonBox(screen, "A", (int(56/800.*WIDTH), int(56/600.*HEIGHT)), (int(7/800.*WIDTH), int((200+55*5/2 - 60)/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\arrowfont.ttf")
    down = textbox.ButtonBox(screen, "V", (int(56/800.*WIDTH), int(56/600.*HEIGHT)), (int(7/800.*WIDTH), int((200+55*5/2 + 4)/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\arrowfont.ttf")

    users = None
    mouse_loc = (0, 0)
    trying = 0
    sub  =False

    done = False                                     #"""the playes exited the game?"""
    start_game = False                               # the game has started?
    pygame.init()
    highlighted = None
    while not start_game and not done: #while game was not exited and game is still at the log in part
        events = pygame.event.get()
        """checks events, user input"""
        for event in events:#checks for events including:
            if event.type == MouseMotion:#mouse hovering above the start button
                x, y = event.pos
                mouse_loc = event.pos

            if event.type == pygame.QUIT:#user presses the X
                done = True
                exit()
            if event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    done = True
                    exit()
        """"load screen"""
        screen.fill((237, 43, 0))


        a.draw()
        Play.draw()
        Edit.draw()
        up.draw()
        down.draw()
        for quizon in quizes:
            quizon.draw()
        moved = False
        if up.was_clicked():
            time.sleep(0.1)
            n -= 1
            if n<0:
                n+=1
            moved = True
        if down.was_clicked():
            time.sleep(0.1)
            n += 1
            if n>=len(onlyfiles)-4:
                n-=1
            moved = True

        counter = 0
        for quizon in quizes:
            try:
                if quizon.was_clicked():
                    highlighted = n+counter
                    moved = True
            except Exception:
                pass
            counter += 1

        print highlighted

        if moved:
            quizes = []
            onlyfiles = [f for f in os.listdir("dependencies\\quizes") if os.path.isfile(os.path.join("dependencies\\quizes", f))]
            onlyfiles = sorted(onlyfiles)
            counter = 0
            for file in onlyfiles[n:n+5]:
                if n < 0:
                    n = len(onlyfiles) - 1
                if n+counter != highlighted:
                    quizes.append(textbox.ButtonBox(screen, file.split(".json")[0], (int(2*WIDTH/3), int(50/600.*HEIGHT)), (int(75/800.*WIDTH), int((200+55*counter)/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf"))
                else:
                    quizes.append(textbox.OutputBox(screen, file.split(".json")[0], (int(2*WIDTH/3), int(50/600.*HEIGHT)), (int(75/800.*WIDTH), int((200+55*counter)/600.*HEIGHT)), (255, 255, 255), 5, (0, 100, 255), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf"))
                counter += 1



        pygame.display.flip()

        if trying >= WIDTH/10:
            sub = True
        if trying <= -20:
            sub = False

        if not sub:
            trying += 0.5
        else:
            trying -= 0.5
        clock.tick(24)


if __name__ == '__main__':
    main()