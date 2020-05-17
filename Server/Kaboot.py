import pygame
from pygame.locals import *
import time
import os
from dependencies.files import textbox
from dependencies import Quizmatron, Game
import json
import base64
import Tkinter
import tkSimpleDialog
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
    #Play = textbox.ButtonBox(screen, "Play!", (int((770-25)/800.*WIDTH)/2, int(580/600.*HEIGHT-490/600.*HEIGHT)), (int(25/800.*WIDTH), int(490/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf")
    Play = textbox.ButtonBox(screen, "Play!", (int((770-25)/800.*WIDTH), int(580/600.*HEIGHT-490/600.*HEIGHT)), (int(25/800.*WIDTH), int(490/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf")
    Edit = textbox.ButtonBox(screen, "Edit...", (int((770-25)/800.*WIDTH)/2, int(580/600.*HEIGHT-490/600.*HEIGHT)), (int(800-25/800.*WIDTH) - int((770-25)/800.*WIDTH)/2, int(490/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf")


    onlyfiles = [f for f in os.listdir("dependencies\\quizes") if os.path.isfile(os.path.join("dependencies\\quizes", f))]
    onlyfiles = sorted(onlyfiles)
    quizes = []
    n = 0
    counter = 0
    for file in onlyfiles[n:n+5]:
        if n < 0:
            n = len(onlyfiles) - 1
        quizes.append(textbox.ButtonBox(screen, file.split(".json")[0], (int(2*WIDTH/3), int(50/600.*HEIGHT)), (int(75/800.*WIDTH), int((200+55*counter)/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf"))
        counter += 1

    quizestitle = textbox.OutputBox(screen, "Quizzes:", (int(130/800.*WIDTH), int(45/600.*HEIGHT)), (int(75/800.*WIDTH), int(155/600.*HEIGHT)), None, 0, None, (255, 255, 255), "dependencies\\files\\montserrat\\Montserrat-Black.otf")

    up = textbox.ButtonBox(screen, "A", (int(56/800.*WIDTH), int(56/600.*HEIGHT)), (int(7/800.*WIDTH), int((200+55*5/2 - 60)/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\arrowfont.ttf")
    down = textbox.ButtonBox(screen, "V", (int(56/800.*WIDTH), int(56/600.*HEIGHT)), (int(7/800.*WIDTH), int((200+55*5/2 + 4)/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\arrowfont.ttf")

    newlizatzia = textbox.ButtonBox(screen, "+new quiz", (int(172/800.*WIDTH), int(50/600.*HEIGHT)), (int(620/800.*WIDTH), int(200+55*0/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf")
    #importazia = textbox.ButtonBox(screen, "+Import", (int(172/800.*WIDTH), int(50/600.*HEIGHT)), (int(620/800.*WIDTH), int(200+55*1/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf")
    renamezatzia = textbox.ButtonBox(screen, "Rename", (int(172/800.*WIDTH), int(50/600.*HEIGHT)), (int(620/800.*WIDTH), int(200+55*2/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf")
    deletazione = textbox.ButtonBox(screen, "Delete", (int(172/800.*WIDTH), int(50/600.*HEIGHT)), (int(620/800.*WIDTH), int(200+55*3/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf")
    Edit = textbox.ButtonBox(screen, "Edit", (int(172/800.*WIDTH), int(50/600.*HEIGHT)), (int(620/800.*WIDTH), int(200+55*4/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf")
    #exportatzia = textbox.ButtonBox(screen, "Export ->", (int(172/800.*WIDTH), int(50/600.*HEIGHT)), (int(620/800.*WIDTH), int(200+55*4/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf")

    namechageA = textbox.InputBox(screen, (int(2*WIDTH/3), int(60/600.*HEIGHT)), (int(WIDTH/6.), int(300/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf", allow_enter=False)

    save = textbox.ButtonBox(screen, "Save!", (int((770-25)/800.*WIDTH)/2, int(580/600.*HEIGHT-490/600.*HEIGHT)), (int(25/800.*WIDTH), int(490/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf")
    cancel = textbox.ButtonBox(screen, "Cancel...", (int((770-25)/800.*WIDTH)/2, int(580/600.*HEIGHT-490/600.*HEIGHT)), (int(800-25/800.*WIDTH) - int((770-25)/800.*WIDTH)/2, int(490/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf")

    trying = 0
    sub  =False

    done = False                                     #"""the playes exited the game?"""
    start_game = False                               # the game has started?
    pygame.init()
    highlighted = None
    namechage = False
    newquiz = False
    buff = False
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
        screen.fill((201, 14, 163))


        a.draw()
        if not namechage and not newquiz:
            up.draw()
            down.draw()
            quizestitle.draw()
            newlizatzia.draw()
            #importazia.draw()

            for quizon in quizes:
                quizon.draw()

            if highlighted or highlighted == 0:
                Play.draw()
                Edit.draw()
                renamezatzia.draw()
                deletazione.draw()
                #exportatzia.draw()


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

        if deletazione.was_clicked():
            if highlighted == len(onlyfiles) - 1:
                n -= 1
            os.remove("dependencies\\quizes\\" + onlyfiles[highlighted])
            highlighted = None
            moved = True

        if renamezatzia.was_clicked():
            namechage = True

        if namechage:
            textbox.OutputBox(screen, "Choose a new name for the quiz \"" + onlyfiles[highlighted].split(".json")[0] + "\":", (int(750/800.*WIDTH), int(50/600.*HEIGHT)), (int(25/800.*WIDTH), int((230)/600.*HEIGHT)), None, 0, None, (0, 255, 255), "dependencies\\files\\montserrat\\Montserrat-Black.otf").draw()
            namechageA.draw()
            save.text = "Save!"
            if namechageA.get_input() + ".json" in onlyfiles:
                textbox.OutputBox(screen, "A quiz by that name already exists!", (int(750/800.*WIDTH), int(50/600.*HEIGHT)), (int(25/800.*WIDTH), int((400)/600.*HEIGHT)), None, 0, None, (255, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf").draw()
            else:
                if namechageA.get_input():
                    save.draw()
            cancel.draw()
            namechageA.inputted_text = namechageA.get_input().replace("/", "").replace("\\", "").replace("*", "").replace(":", "").replace("?", "").replace("\"", "").replace(">", "").replace("<", "").replace("|", "")
            if save.was_clicked():
                os.rename("dependencies\\quizes\\" + onlyfiles[highlighted], "dependencies\\quizes\\" + namechageA.get_input() + ".json")
                namechage = False
                namechageA.inputted_text = ""
                moved = True
                buff = True
            if cancel.was_clicked():
                namechage = False
                namechageA.inputted_text = ""
                moved = True
                buff = True


        if newlizatzia.was_clicked():
            newquiz = True

        if newquiz:
            textbox.OutputBox(screen, "Choose a name for the new quiz you are creating:", (int(750/800.*WIDTH), int(50/600.*HEIGHT)), (int(25/800.*WIDTH), int((230)/600.*HEIGHT)), None, 0, None, (0, 255, 255), "dependencies\\files\\montserrat\\Montserrat-Black.otf").draw()
            namechageA.draw()
            save.text = "Create!"
            if namechageA.get_input() + ".json" in onlyfiles:
                textbox.OutputBox(screen, "A quiz by that name already exists!", (int(750/800.*WIDTH), int(50/600.*HEIGHT)), (int(25/800.*WIDTH), int((400)/600.*HEIGHT)), None, 0, None, (255, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf").draw()
            else:
                if namechageA.get_input():
                    save.draw()
            cancel.draw()
            namechageA.inputted_text = namechageA.get_input().replace("/", "").replace("\\", "").replace("*", "").replace(":", "").replace("?", "").replace("\"", "").replace(">", "").replace("<", "").replace("|", "")
            if save.was_clicked():
                qname = namechageA.get_input()
                with open("dependencies\\quizes\\" + qname + ".json", 'wb') as qfile:
                    json.dump({"Questions":
                                    [
                                        {
                                            "time to answer": 60,
                                            "points": 100,
                                            "image file type": None,
                                            "photo": None,
                                            "correct answer": 1,
                                            "question": "?",
                                            "time to read": 5,
                                            "answers": [
                                                "1",
                                                "2",
                                                "3",
                                                "4"
                                            ]
                                        }
                                    ]
                                }, qfile, indent=4)
                newquiz = False
                moved = True
                namechageA.inputted_text = ""
                Quizmatron.main(qname)
            if cancel.was_clicked():
                newquiz = False
                moved = True
                namechageA.inputted_text = ""
                buff = True

        if not buff:
            if Edit.was_clicked() and not (namechage or newquiz):
                Quizmatron.main(onlyfiles[highlighted].split(".json")[0])

            if Play.was_clicked() and not (namechage or newquiz):
                Game.main(onlyfiles[highlighted].split(".json")[0])

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
                    quizes.append(textbox.OutputBox(screen, file.split(".json")[0], (int(2*WIDTH/3), int(50/600.*HEIGHT)), (int(75/800.*WIDTH), int((200+55*counter)/600.*HEIGHT)), (255, 255, 255), 5, (255, 255, 50), (0, 0, 0), "dependencies\\files\\montserrat\\Montserrat-Black.otf"))
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
        if buff:
            buff = False
            time.sleep(0.3)

if __name__ == '__main__':
    main()