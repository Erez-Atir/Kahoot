IP = None
my_socket = None
import os
import sys
sys.path.insert(0, os.getcwd()+'/files')
sys.dont_write_bytecode = True
import ServerDitection
import socket
import pygame
import textbox
import subprocess


RED = (204, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 153, 0)
BLUE = (53, 119, 252)
PURPLE = (176, 71, 246)
GREY = (85, 77, 77)
ORANGE = (255, 181, 30)


def resfix(x=None, y=None):
    """
    :param x: the x coordinate or a Pygame image. If sent None means only y need a conversion
    :param y: the y coordinate. can be not sent for only x conversion.
    :return: The new coordinates on the new screen with the same proportions. Tuple for (x,y). int for only one number.
    """
    global WIDTH, HEIGHT
    if x is not None:
        if type(x) == type(42):
            if y is not None:
                return int(x/1500.*WIDTH), int(y/800.*HEIGHT)
            return int(x/1500.*WIDTH)
        else:
            sizee = x.get_rect().size
            return
    if y is not None:
        return int(y/800.*HEIGHT)
    return None

if True:
    IP = ServerDitection.server_scout()
    if IP:
        my_socket = socket.socket()
        my_socket.connect((IP, 23))
    else:


        screen = pygame.display.set_mode((1500, 800))
        WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        pygame.display.set_caption("Kaboot")
        screen.fill(PURPLE)
        a = textbox.OutputBox(screen=screen, text="No Game\nRunning!", size=resfix(650, 750), place=resfix(825, 0), color=None,
                              border_width=0, border_color=None, text_color=RED, font="files\\montserrat\\Montserrat-Black.otf")
        b = textbox.OutputBox(screen=screen, text="Ask your teacher to run a game and then try again", size=resfix(650, 750), place=resfix(825, 0), color=None,
                              border_width=0, border_color=None, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf")
        c = textbox.OutputBox(screen=screen, text="  EXIT  ", size=resfix(310, 100), place=resfix((825+(825+650))/2-310/2, 600), color=WHITE,
                              border_width=0, border_color=BLACK, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf")
        img = pygame.transform.scale(pygame.image.load("files\\sadog.jpg"), (int(WIDTH*1.066), HEIGHT))
        finish = False
        while not finish:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:#user presses the X
                    exit()
                if event.type == pygame.KEYDOWN:
                    # If pressed key is ESC quit program
                    if event.key == pygame.K_ESCAPE:
                        exit()
            if resfix((825+(825+650))/2-310/2+310) > mouse[0] > resfix((825+(825+650))/2-310/2) and resfix(None, 600+100) > mouse[1] > resfix(None, 600):
                c.border_width = 5
                if pygame.mouse.get_pressed()[0]:
                    sys.exit()
            else:
                c.border_width = 0
            screen.blit(img, (0, 0))
            a.draw()
            b.draw()
            c.draw()
            pygame.display.flip()