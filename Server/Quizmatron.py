import pygame
from pygame.locals import *
import time
import os
from files import textbox
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


def main(QUIZ):
    global users, TotalQN, quiz
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
        done = load_question(screen, question, photype, answers, qtime, points, timer, 0)  # calls a function to print the question
        return done


def load_question(screen, question, photo, answers, qtime, points, rtime, QuestioNumber):
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

    global users, quiz
    # image

    rc = pygame.image.load(IMAGES_DIR + "main\\red_correct.png")
    rc = pygame.transform.scale(rc, (396, 112))
    bc = pygame.image.load(IMAGES_DIR + "main\\blue_correct.png")
    bc = pygame.transform.scale(bc, (396, 112))
    yc = pygame.image.load(IMAGES_DIR + "main\\orange_correct.png")
    yc = pygame.transform.scale(yc, (396, 112))
    gc = pygame.image.load(IMAGES_DIR + "main\\green_correct.png")
    gc = pygame.transform.scale(gc, (396, 112))
    sx, sy = (396, 112)
    a = [0, 367, 403, 367, 0, 484, 403, 484]
    Rstartx, Rstarty, Bstartx, Bstarty, Ystartx, Ystarty, Gstartx, Gstarty = [int(a[x]/800.*WIDTH) if x % 2 == 0 else int(a[x]/600.*HEIGHT) for x in range(len(a))]
    addedimg = None
    if photo:
        addedimg = pygame.transform.scale(pygame.image.load("./files/temp." + photo), (int((665-143)/800.*WIDTH), int((334-70)/600.*HEIGHT)))
    imgbutt = textbox.ButtonBox(screen, text="", place=(int(143/800.*WIDTH), int(75/600.*HEIGHT)), size=(int((665-143)/800.*WIDTH),  int((334-75)/600.*HEIGHT)), color=None, text_color=(0, 0, 0), border_color=(0, 0, 0), border_width=2, mouse=False)
    uploadimg = pygame.transform.scale(pygame.image.load(IMAGES_DIR + "icons\\upload_image.png"), (int((665-143)/800.*WIDTH/4), int((334-70+60)/600.*HEIGHT/3)))
    uploadimgbutt = textbox.ButtonBox(screen, text="", place=(int(143/800.*WIDTH)+int((665-143)/800.*WIDTH)*0.55, int(75-20/600.*HEIGHT)+int((334-70)/600.*HEIGHT)*0.3), size=(int((665-143)/800.*WIDTH/4), int((334-70+60)/600.*HEIGHT/3)), color=None, text_color=(0, 0, 0), border_color=None, border_width=0)
    delimg = pygame.transform.scale(pygame.image.load(IMAGES_DIR + "icons\\x.png"), (int((665-143)/800.*WIDTH/4), int((334-70)/600.*HEIGHT/3)))
    delimgbutt = textbox.ButtonBox(screen, text="", place=(int(143/800.*WIDTH)+int((665-143)/800.*WIDTH)*0.20, int(75/600.*HEIGHT)+int((334-70)/600.*HEIGHT)*0.3), size=(int((665-143)/800.*WIDTH/4), int((334-70)/600.*HEIGHT/3)), color=None, text_color=(0, 0, 0), border_color=None, border_width=0)



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
                                          color=WHITE, text_color=BLACK, border_color=BLACK, border_width=2, font="files\\montserrat\\Montserrat-Black.otf", numeric=True, placeholder=str(rtime))
    TimeToAnswerQ = textbox.OutputBox(screen, text=" Seconds\nto answer:", size=(int(140/800.*WIDTH), int((296/6)/600.*HEIGHT)), place=(int(2/800.*WIDTH), int((70+int((296/6)/600.*HEIGHT)*2+5)/600.*HEIGHT)),
                                      color=None, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf")
    TimeToAnswerA = textbox.InputBox(screen, size=(int(140/800.*WIDTH), int((296/6)/600.*HEIGHT)), place=(int(2/800.*WIDTH), int((70+int((296/6)/600.*HEIGHT)*2+298/6+5)/600.*HEIGHT)),
                                          color=WHITE, text_color=BLACK, border_color=BLACK, border_width=2, font="files\\montserrat\\Montserrat-Black.otf", numeric=True, placeholder=str(qtime))
    prev = textbox.ButtonBox(screen, text="<-", size=(int((753-693-6)/800.*WIDTH), int((235-175)/600.*HEIGHT)), place=(int((43+3)/800.*WIDTH), int((366-(235-170)-20)/600.*HEIGHT)),
                                              color=None, text_color=WHITE, border_color=None, font="files\\montserrat\\Montserrat-Black.otf")


    PointsQ = textbox.OutputBox(screen, text=" Reward:", size=(int(132/800.*WIDTH), int((296/6)/600.*HEIGHT)), place=(int(666/800.*WIDTH), int((70)/600.*HEIGHT)),
                                          color=None, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf")
    PointsA = textbox.InputBox(screen, size=(int(132/800.*WIDTH), int((296/6)/600.*HEIGHT)), place=(int(666/800.*WIDTH), int((70+298/6)/600.*HEIGHT)),
                                          color=WHITE, text_color=BLACK, border_color=BLACK, border_width=2, font="files\\montserrat\\Montserrat-Black.otf", numeric=True, placeholder=str(points))

    nothing = textbox.OutputBox(screen, text="place saver", size=(int(132/800.*WIDTH), int((296/6)/600.*HEIGHT)), place=(int(666/800.*WIDTH), int((70+int((296/6)/600.*HEIGHT)*2+5)/600.*HEIGHT)),
                                        color=None, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf")
    BackToHomeScreen = textbox.ButtonBox(screen, text="Back To\nHome Screen", size=(int(132/800.*WIDTH), int((296/6)/600.*HEIGHT)), place=(int(666/800.*WIDTH), int((70+int((296/6)/600.*HEIGHT)*2+298/6+5)/600.*HEIGHT) - int((296/6)/600.*HEIGHT)/2),
                                          color=(201, 14, 163), text_color=WHITE, border_color=None, border_width=2, font="files\\montserrat\\Montserrat-Black.otf")
    next = textbox.ButtonBox(screen, text="->", size=(int((753-693-6)/800.*WIDTH), int((235-175)/600.*HEIGHT)), place=(int((693+3)/800.*WIDTH), int((366-(235-170)-20)/600.*HEIGHT)),
                                              color=None, text_color=WHITE, border_color=None, font="files\\montserrat\\Montserrat-Black.otf")


    rb = textbox.ButtonBox(screen, text="", place=(9, 397), size=(44, 41), color=None, text_color=(0, 0, 0), border_color=None)
    bb = textbox.ButtonBox(screen, text="", place=(411, 395), size=(46, 46), color=None, text_color=(0, 0, 0), border_color=None)
    yb = textbox.ButtonBox(screen, text="", place=(10, 516), size=(46, 46), color=None, text_color=(0, 0, 0), border_color=None)
    gb = textbox.ButtonBox(screen, text="", place=(414, 519), size=(45, 43), color=None, text_color=(0, 0, 0), border_color=None)

    regretometer = 0
    wtf = False
    idk = False
    counter = 3
    changes = False
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

        if quiz["Questions"][QuestioNumber]["correct answer"] == 1:
            pygame.draw.rect(screen, (29, 161, 29), (Rstartx, Rstarty, sx, sy))
        screen.blit(rc, (Rstartx, Rstarty))
        if quiz["Questions"][QuestioNumber]["correct answer"] == 2:
            pygame.draw.rect(screen, (29, 161, 29), (Bstartx, Bstarty, sx, sy))
        screen.blit(bc, (Bstartx, Bstarty))
        if quiz["Questions"][QuestioNumber]["correct answer"] == 3:
            pygame.draw.rect(screen, (29, 161, 29), (Ystartx, Ystarty, sx, sy))
        screen.blit(yc, (Ystartx, Ystarty))
        if quiz["Questions"][QuestioNumber]["correct answer"] == 4:
            pygame.draw.rect(screen, (29, 161, 29), (Gstartx, Gstarty, sx, sy))
        screen.blit(gc, (Gstartx, Gstarty))


        # question
        question_text.draw()
        if question_text.get_input() != quiz["Questions"][QuestioNumber]["question"]:
            quiz["Questions"][QuestioNumber]["question"] = question_text.get_input()
            changes = True
            #print "1"

        # answers
        numbbbbbbb = 0
        for answer in answer_boxes:
            answer.draw()
            if answer.get_input() != quiz["Questions"][QuestioNumber]["answers"][numbbbbbbb]:
                quiz["Questions"][QuestioNumber]["answers"][numbbbbbbb] = answer.get_input()
                changes = True
                #print "2"
            numbbbbbbb += 1



        for button in [BackToHomeScreen, prev, next]:
            if button.is_highlighted():
                button.text_color = BLACK
            else:
                button.text_color = WHITE

        TimeToAnswerQ.draw()
        TimeToAnswerA.draw()
        if TimeToAnswerA.get_input() and int(TimeToAnswerA.get_input()) != quiz["Questions"][QuestioNumber]["time to answer"]:
            quiz["Questions"][QuestioNumber]["time to answer"] = int(TimeToAnswerA.get_input())
            changes = True
            #print "3"
        TimeToReadQ.draw()
        TimeToReadA.draw()
        if TimeToReadA.get_input() and int(TimeToReadA.get_input()) != quiz["Questions"][QuestioNumber]["time to read"]:
            quiz["Questions"][QuestioNumber]["time to read"] = int(TimeToReadA.get_input())
            changes = True
            #print "4"
        prev.draw()

        PointsQ.draw()
        PointsA.draw()
        if PointsA.get_input() and int(PointsA.get_input()) != quiz["Questions"][QuestioNumber]["points"]:
            quiz["Questions"][QuestioNumber]["points"] = int(PointsA.get_input())
            changes = True
            #print "5"
        BackToHomeScreen.draw()
        next.draw()

        rb.draw()
        bb.draw()
        yb.draw()
        gb.draw()
        if rb.was_clicked():
            quiz["Questions"][QuestioNumber]["correct answer"] = 1
            changes = True
            #print "6"
        if bb.was_clicked():
            quiz["Questions"][QuestioNumber]["correct answer"] = 2
            changes = True
            #print "7"
        if yb.was_clicked():
            quiz["Questions"][QuestioNumber]["correct answer"] = 3
            changes = True
            #print "8"
        if gb.was_clicked():
            quiz["Questions"][QuestioNumber]["correct answer"] = 4
            changes = True
            #print "9"

        imgbutt.draw()
        if imgbutt.is_highlighted():
            screen.blit(uploadimg, (int(143/800.*WIDTH)+int((665-143)/800.*WIDTH)*0.55, int(75-20/600.*HEIGHT)+int((334-70)/600.*HEIGHT)*0.3))
            screen.blit(delimg, (int(143/800.*WIDTH)+int((665-143)/800.*WIDTH)*0.20, int(75/600.*HEIGHT)+int((334-70)/600.*HEIGHT)*0.3))

        uploadimgbutt.draw()
        delimgbutt.draw()

        if wtf:
            counter -= 1
            if counter == 0:
                Tk().withdraw()
                file = tkFileDialog.askopenfilename(initialdir="/Pictures", title="Choose Image To Upload", filetypes=[("image files", ".jpg .png")])
                results = []
                top_windows = []
                win32gui.EnumWindows(windowEnumerationHandler, top_windows)
                for i in top_windows:
                    if "kaboot" in i[1].lower():
                        win32gui.ShowWindow(i[0], 5)
                        win32gui.SetForegroundWindow(i[0])
                        break
                if file:
                    imaging(screen, file, screen.copy())
                    previmg = addedimg
                    addedimg = addedimg = pygame.transform.scale(pygame.image.load("./files/temp." + "jpg"), (int((665-143)/800.*WIDTH), int((334-70)/600.*HEIGHT)))
                    regretometer = 3
                wtf = False
                counter = 3
        if uploadimgbutt.was_clicked():
            wtf = True

        if idk:
            counter -= 1
            if counter == 0:
                Tk().withdraw()
                delimgwindow = tkMessageBox.askyesno("Remove Image", "Are you sure you want to remove the existing image?\nThis action cannot be reversed!")
                if delimgwindow:
                    addedimg = None
                    quiz['Questions'][QuestioNumber]['photo'] = None
                    quiz['Questions'][QuestioNumber]['image file type'] = None
                    changes = True
                    #print "10"
                idk = False
                counter = 3
        if delimgbutt.was_clicked() and addedimg:
            idk = True


        if regretometer == 3:
            regretometer = 2
        elif regretometer == 2:
            regretometer = 1
        elif regretometer == 1:
            Tk().withdraw()
            swich = tkMessageBox.askokcancel("Preview of New Image", "Are you sure you want to change the image?\nThis action cannot be reversed!")
            if swich:
                with open("./files/temp." + "jpg", 'rb') as img:
                    quiz['Questions'][QuestioNumber]['photo'] = base64.b64encode(img.read())
                    quiz['Questions'][QuestioNumber]['image file type'] = "jpg"
                    changes = True
                    #print "11"
            else:
                addedimg = previmg
            regretometer = 0

        if changes:
            #print "updated"
            with open('quizes/test.json', 'wb') as qfile:
                json.dump(quiz, qfile, indent=4)
        changes = False
        #check_for_place(screen, events)
        pygame.display.flip()
        clock.tick(60)
    pygame.mixer.music.stop()
    return False


def imaging(screen, file, background):
    global quiz

    background = background.convert()
    background.set_alpha(20)

    question_text = textbox.OutputBox(screen, "Use + and - to change the image's scale.\nUse the mouse to move the image.", (WIDTH, int(75/600.*HEIGHT)), (0, 0), (0, 0, 0), 0, (), (255, 255, 255), "files\\montserrat\\Montserrat-Black.otf")
    doneb = textbox.ButtonBox(screen, "Done", (int(770/800.*WIDTH-25/800.*WIDTH), int(580/600.*HEIGHT-490/600.*HEIGHT)), (int(25/800.*WIDTH), int(490/600.*HEIGHT)), (255, 255, 255), 5, (0, 0, 0), (0, 0, 0), "files\\montserrat\\Montserrat-Black.otf")
    frame = textbox.OutputBox(screen, text="", size=(int((665-143)/800.*WIDTH), int((334-75)/600.*HEIGHT)), place=(int(143/800.*WIDTH), int(75/600.*HEIGHT)),
                                          color=None, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf", border_width=4, border_color=(255, 255, 255))

    image = pygame.image.load(file)
    place = frame.place
    size = image.get_size()
    resize = (1,1)
    if size[0] > size[1]:
        if size[0] > WIDTH:
            resize = (1.*WIDTH/size[0], 1.*WIDTH/size[0])
    else:
        if size[1] > HEIGHT:
            resize = (1.*HEIGHT/size[1], 1.*HEIGHT/size[1])

    finished = False
    mouseinit = None
    while not finished:
        x, y = pygame.mouse.get_pos()
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

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        pressed = pygame.key.get_pressed()
        s,t = resize[0], resize[1]
        for key in pressed:
            if key:
                if pressed.index(1) == 45:
                    if not (pressed[300] or pressed[303]):
                        t = resize[1]-0.005 if resize[1]-0.005 > 0 else t
                    s = resize[0]-0.005 if resize[0]-0.005 > 0 else s
                if pressed.index(1) == 61:
                    if not (pressed[300] or pressed[303]):
                        t = resize[1]+0.01
                    s = resize[0]+0.01
        resize = (s,t)
        if size[0]*resize[0] < frame.size[0] and not size[1]*resize[1] < frame.size[1]:
                    place = (int(frame.place[0]+frame.size[0]/2-(size[0]*resize[0])/2.), place[1])
                    if place[1] > frame.place[1]:
                        place = (place[0], frame.place[1])
                    if place[1] + size[1]*resize[1] < frame.place[1] + frame.size[1]:
                        place = (place[0], frame.place[1]-(size[1]*resize[1]-frame.size[1]))
        elif size[1]*resize[1] < frame.size[1] and not size[0]*resize[0] < frame.size[0]:
                    place = (place[0], int(frame.place[1]+frame.size[1]/2-(size[1]*resize[1])/2.))
                    if place[0] > frame.place[0]:
                        place = (frame.place[0], place[1])
                    if place[0] + size[0]*resize[0] < frame.place[0] + frame.size[0]:
                        place = (frame.place[0]-(size[0]*resize[0]-frame.size[0]), place[1])
        elif size[0]*resize[0] < frame.size[0] and size[1]*resize[1] < frame.size[1]:
            place = (int(frame.place[0]+frame.size[0]/2-(size[0]*resize[0])/2.), int(frame.place[1]+frame.size[1]/2-(size[1]*resize[1])/2.))
        else:
            if size[0]*resize[0] > frame.size[0]:
                        if place[1] + size[1]*resize[1] < frame.place[1] + frame.size[1]:
                            place = (place[0], frame.place[1]-(size[1]*resize[1]-frame.size[1]))
            if size[1]*resize[1] > frame.size[1]:
                        if place[0] + size[0]*resize[0] < frame.place[0] + frame.size[0]:
                            place = (frame.place[0]-(size[0]*resize[0]-frame.size[0]), place[1])

        image = pygame.transform.scale(pygame.image.load(file), (int(size[0]*resize[0]), int(size[1]*resize[1])))
        if pygame.mouse.get_pressed()[0] and (not doneb.is_highlighted() or mouseinit):
            if not mouseinit:
                mouseinit = (x - place[0], y - place[1])
            else:
                if size[0]*resize[0] < frame.size[0] and not size[1]*resize[1] < frame.size[1]:
                    place = (int(frame.place[0]+frame.size[0]/2-(size[0]*resize[0])/2.), y - mouseinit[1])
                    if place[1] > frame.place[1]:
                        place = (place[0], frame.place[1])
                    if place[1] + size[1]*resize[1] < frame.place[1] + frame.size[1]:
                        place = (place[0], frame.place[1]-(size[1]*resize[1]-frame.size[1]))
                elif size[1]*resize[1] < frame.size[1] and not size[0]*resize[0] < frame.size[0]:
                    place = (x - mouseinit[0], int(frame.place[1]+frame.size[1]/2-(size[1]*resize[1])/2.))
                    if place[0] > frame.place[0]:
                        place = (frame.place[0], place[1])
                    if place[0] + size[0]*resize[0] < frame.place[0] + frame.size[0]:
                        place = (frame.place[0]-(size[0]*resize[0]-frame.size[0]), place[1])
                elif size[0]*resize[0] < frame.size[0] and size[1]*resize[1] < frame.size[1]:
                    pass
                else:
                    place = (x - mouseinit[0], y - mouseinit[1])
                    if place[1] > frame.place[1]:
                        place = (place[0], frame.place[1])
                    if place[1] + size[1]*resize[1] < frame.place[1] + frame.size[1]:
                        place = (place[0], frame.place[1]-(size[1]*resize[1]-frame.size[1]))
                    if place[0] > frame.place[0]:
                        place = (frame.place[0], place[1])
                    if place[0] + size[0]*resize[0] < frame.place[0] + frame.size[0]:
                        place = (frame.place[0]-(size[0]*resize[0]-frame.size[0]), place[1])
        else:
            mouseinit = None

        if mouseinit:
            doneb.border_color = None
        else:
            doneb.border_color = (0, 0, 0)

        screen.blit(image, place)
        frame.draw()
        doneb.draw()
        question_text.draw()

        finished = doneb.was_clicked() and not mouseinit

        pygame.display.flip()

    screen.fill((255, 255, 255))
    screen.blit(image, place)
    time.sleep(0.1)
    camera = screen.subsurface(pygame.Rect((frame.place[0], frame.place[1], frame.size[0], frame.size[1])))
    pygame.image.save(camera, "files//temp.jpg")




def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


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
