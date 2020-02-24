import pygame
from pygame.locals import *
import time
import os
from files import textbox
import json
import base64

Title = "test"

PLAYERSSCORE = {} #""""dictionary, saves the points of each player"""
FONT_LIB = pygame.font.match_font('bitstreamverasans')[0:-10] + "\\" #finds the fony libary path
IMAGES_DIR = os.getcwd() + "\\images\\" #saves the path to the images libary
OST_DIR = os.getcwd() + "\\audio\\"
users = None
QuestioNumber = 0
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


def main(QUIZ):
    global users, QuestioNumber, TotalQN
    done = False                                     #"""the playes exited the game?"""
    start_game = False                               # the game has started?
    pygame.init()                                    # initiate pygames

    pygame.display.set_caption("Kaboot")
    pygame.display.flip()
    pygame.font.init()

    a = textbox.OutputBox(screen, QUIZ, (WIDTH, int(100/600.*HEIGHT)), (0, int(50/600.*HEIGHT)), (255, 255, 255), 0, (), (0, 0, 0), "files\\montserrat\\Montserrat-Black.otf")
    c = textbox.OutputBox(screen, "Done", (int(770/800.*WIDTH-25/800.*WIDTH), int(580/600.*HEIGHT-490/600.*HEIGHT)), (int(25/800.*WIDTH), int(490/600.*HEIGHT)), (255, 255, 255), 0, (0, 0, 0), (0, 0, 0), "files\\montserrat\\Montserrat-Black.otf")

    users = None
    mouse_loc = (0, 0)
    trying = 0
    sub  =False
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
            if event.type == MouseButtonDown:#player clicks the screen(should be only button)
                if event.button == 1:
                    x, y = event.pos
                    if 25/800.*WIDTH < x and x < 770/800.*WIDTH and y > 490/600.*HEIGHT and y < 580/600.*HEIGHT:   # if mouse above start button
                        start_game = True
        """"load screen"""
        screen.fill((237, 43, 0))
        if trying > 0:
            for x, y in [(x,y) for x in range(-20, 20) for y in range(-20, 20)]:
                pygame.draw.circle(screen, (250, 134, 10), (x*WIDTH/10, y*WIDTH/10), int(trying))
        x, y = mouse_loc                                   #gets mouse location
        if 25/800.*WIDTH < x and x < 770/800.*WIDTH and y > 490/600.*HEIGHT and y < 580/600.*HEIGHT:
            a.draw()
            c.border_width = 6
            c.draw()
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)# set cursor to broken x
        else:
            a.draw()
            c.border_width = 0
            c.draw()
            pygame.mouse.set_cursor(*pygame.cursors.arrow)  # set cursor to an arrow


        pygame.display.flip()

        if trying >= WIDTH/10:
            sub = True
        if trying <= -20:
            sub = False

        if not sub:
            trying += 0.5
        else:
            trying -= 0.5
        clock.tick(60)

    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    with open('quizes/' + QUIZ + '.json', 'rb') as qfile:
        quiz = json.load(qfile)

    #with open(IMAGES_DIR+"Example.jpg", 'rb') as img:
    #    quiz['Questions'][0]['photo'] = base64.b64encode(img.read())
    #with open('quizes/test.json', 'wb') as qfile:
    #    json.dump(quiz, qfile, indent=4)

    pygame.mixer.music.fadeout(quiz['Questions'][0]['time to read']*1000)

    TotalQN = len(quiz['Questions'])
    for q in quiz['Questions']:
        add_question(screen, q['time to read'], q['question'], [x.encode("utf-8") for x in q['answers']], q['correct answer'], q['photo'], q['image file type'], q['time to answer'], q['points'])
        first = False


    exit()


def add_question(screen, timer, question, answers, correct_answer, photo, photype, qtime, points):
        """
        function that adds a question to the game
        :param screen: gets the screen obj to print on
        :param timer:  gets the amount of time before question
        :param question: gets the question (no longer than 40 letters)
        :param answers:  gets the possible answers
        :param correct_answer:  gets the number of the correct answer
        :param photo: gets a photo that's relevant to the question
        :param qtime: gets time to answer the question
        :param points: gets the maximum points received py this question
        :return: Was the server closed
        """

        if photo and photype:
            with open("files/temp." + photype, "wb") as temp:
                temp.write(base64.b64decode(photo))
        done = load_question(screen, question, photo, answers, qtime)  # calls a function to print the question
        return done


def load_question(screen, question, photo, answers, qtime):
    """

    :param screen: gets screen to print on
    :param question: gets the question
    :param photo: gets a photo if there is one
    :param answers: gets all possible answers
    :param correct_answer: gets the number of the correct answer
    :param qtime: gets the time for the question
    :param qpoints: gets maximum points for answering the question
    :return: Did player exit the game
    """

    global users
    # image

    rc = pygame.image.load(IMAGES_DIR + "main\\red_correct.png")
    rc = resfix(rc)
    bc = pygame.image.load(IMAGES_DIR + "main\\blue_correct.png")
    bc = resfix(bc)
    yc = pygame.image.load(IMAGES_DIR + "main\\orange_correct.png")
    yc = resfix(yc)
    gc = pygame.image.load(IMAGES_DIR + "main\\green_correct.png")
    gc = resfix(gc)
    a = [0, 367, 403, 367, 0, 484, 403, 484]
    Rstartx, Rstarty, Bstartx, Bstarty, Ystartx, Ystarty, Gstartx, Gstarty = [int(a[x]/800.*WIDTH) if x % 2 == 0 else int(a[x]/600.*HEIGHT) for x in range(len(a))]
    addedimg = None
    if photo:
        addedimg = pygame.transform.scale(pygame.image.load("./files/temp.jpg"), (int((665-143)/800.*WIDTH), int((334-70)/600.*HEIGHT)))


    # question
    question_text = textbox.InputBox(screen, (WIDTH, int(70/600.*HEIGHT)), (0, 0), (255, 255, 255), 0, (), (0, 0, 0), "files\\montserrat\\Montserrat-Black.otf", False, question)
    # time

    answer_boxes = []
    for y in range(4):
        answer_boxes.append(textbox.InputBox(screen, placeholder=answers[y], size=(int(335/800.*WIDTH), int(105/600.*HEIGHT)), place=(int(int(60/800.*WIDTH) + (WIDTH / 2) * (y % 2)), int(372/600.*HEIGHT) + int(120/600.*HEIGHT) * int(y / 2)),
                                              color=None, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf"))


    TimeToReadQ = textbox.OutputBox(screen, text=" Seconds\nto read:", size=(int(140/800.*WIDTH), int((296/6)/600.*HEIGHT)), place=(int(2/800.*WIDTH), int((70)/600.*HEIGHT)),
                                          color=None, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf")
    TimeToReadA = textbox.InputBox(screen, size=(int(140/800.*WIDTH), int((296/6)/600.*HEIGHT)), place=(int(2/800.*WIDTH), int((70+298/6)/600.*HEIGHT)),
                                          color=WHITE, text_color=BLACK, border_color=BLACK, border_width=2, font="files\\montserrat\\Montserrat-Black.otf", numeric=True)
    TimeToAnswerQ = textbox.OutputBox(screen, text=" Seconds\nto answer:", size=(int(140/800.*WIDTH), int((296/6)/600.*HEIGHT)), place=(int(2/800.*WIDTH), int((70+int((296/6)/600.*HEIGHT)*2+5)/600.*HEIGHT)),
                                      color=None, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf")
    TimeToAnswerA = textbox.InputBox(screen, size=(int(140/800.*WIDTH), int((296/6)/600.*HEIGHT)), place=(int(2/800.*WIDTH), int((70+int((296/6)/600.*HEIGHT)*2+298/6+5)/600.*HEIGHT)),
                                          color=WHITE, text_color=BLACK, border_color=BLACK, border_width=2, font="files\\montserrat\\Montserrat-Black.otf", numeric=True)
    prev = textbox.ButtonBox(screen, text="<-", size=(int((753-693-6)/800.*WIDTH), int((235-175)/600.*HEIGHT)), place=(int((43+3)/800.*WIDTH), int((366-(235-170)-20)/600.*HEIGHT)),
                                              color=None, text_color=WHITE, border_color=None, font="files\\montserrat\\Montserrat-Black.otf")


    PointsQ = textbox.OutputBox(screen, text=" Reward:", size=(int(138/800.*WIDTH), int((296/6)/600.*HEIGHT)), place=(int(660/800.*WIDTH), int((70)/600.*HEIGHT)),
                                          color=None, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf")
    PointsA = textbox.InputBox(screen, size=(int(138/800.*WIDTH), int((296/6)/600.*HEIGHT)), place=(int(660/800.*WIDTH), int((70+298/6)/600.*HEIGHT)),
                                          color=WHITE, text_color=BLACK, border_color=BLACK, border_width=2, font="files\\montserrat\\Montserrat-Black.otf", numeric=True)

    nothing = textbox.OutputBox(screen, text="place saver", size=(int(138/800.*WIDTH), int((296/6)/600.*HEIGHT)), place=(int(660/800.*WIDTH), int((70+int((296/6)/600.*HEIGHT)*2+5)/600.*HEIGHT)),
                                        color=None, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf")
    BackToHomeScreen = textbox.ButtonBox(screen, text="Back To\nMain Screen", size=(int(138/800.*WIDTH), int((296/6)/600.*HEIGHT)), place=(int(660/800.*WIDTH), int((70+int((296/6)/600.*HEIGHT)*2+298/6+5)/600.*HEIGHT) - int((296/6)/600.*HEIGHT)/2),
                                          color=(201, 14, 163), text_color=WHITE, border_color=None, border_width=2, font="files\\montserrat\\Montserrat-Black.otf")
    next = textbox.ButtonBox(screen, text="->", size=(int((753-693-6)/800.*WIDTH), int((235-175)/600.*HEIGHT)), place=(int((693+3)/800.*WIDTH), int((366-(235-170)-20)/600.*HEIGHT)),
                                              color=None, text_color=WHITE, border_color=None, font="files\\montserrat\\Montserrat-Black.otf")

    answers_amount = 0
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                exit()
                return True
            if event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    exit()
                    return True

        screen.fill(WHITE)
        pygame.draw.circle(screen, (201, 14, 163), (int(723 / 800. * WIDTH), int((366-30-20) / 600. * HEIGHT)), 30)
        pygame.draw.circle(screen, (201, 14, 163), (int(74 / 800. * WIDTH), int((366-30-20) / 600. * HEIGHT)), 30)
        if addedimg:
            screen.blit(addedimg, (int(143/800.*WIDTH), int(75/600.*HEIGHT)))
        else:
            textbox.OutputBox(screen, text=" KABOOT! ", size=(int((665-143)/800.*WIDTH), int((334-75)/600.*HEIGHT)), place=(int(143/800.*WIDTH), int(75/600.*HEIGHT)),
                                          color=(201, 14, 163), text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf").draw()

        screen.blit(rc, (Rstartx, Rstarty))
        screen.blit(bc, (Bstartx, Bstarty))
        screen.blit(yc, (Ystartx, Ystarty))
        screen.blit(gc, (Gstartx, Gstarty))

        #check_for_place(screen, events)

        # question
        question_text.draw()

        # answers
        for answer in answer_boxes:
            answer.draw()


        for button in [BackToHomeScreen, prev, next]:
            if button.is_highlighted():
                button.text_color = BLACK
            else:
                button.text_color = WHITE

        TimeToAnswerQ.draw()
        TimeToAnswerA.draw()
        TimeToReadQ.draw()
        TimeToReadA.draw()
        prev.draw()

        PointsQ.draw()
        PointsA.draw()
        BackToHomeScreen.draw()
        next.draw()


        pygame.display.flip()
    pygame.mixer.music.stop()
    return False





def get_font(name):
    return FONT_LIB + name + ".ttf"


def check_for_place(screen, events, width=1):
    pos = pygame.mouse.get_pos()
    for event in events:
        if event.type == MouseButtonDown:#player clicks the screen(should be only button)
            if event.button == 1:
                print pos

    pygame.draw.line(screen, (0, 0, 0), (pos[0], 0), (pos[0], HEIGHT), width)
    pygame.draw.line(screen, (0, 0, 0), (0, pos[1]), (WIDTH, pos[1]), width)


def resfix(image):
    size = image.get_rect().size
    return pygame.transform.scale(image, (int(size[0]/800.*WIDTH), int(size[1]/600.*HEIGHT)))


main(Title)
