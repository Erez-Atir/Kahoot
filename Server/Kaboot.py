import pygame
from pygame.locals import *
import time
import os
from files import Server
from files import textbox
import json
import base64


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


def main():
    global users, QuestioNumber, TotalQN
    done = False                                     #"""the playes exited the game?"""
    start_game = False                               # the game has started?
    pygame.init()                                    # initiate pygames

    pygame.display.set_caption("Kaboot")
    pygame.display.flip()
    pygame.font.init()

    a = textbox.OutputBox(screen, "KABOOT!", (WIDTH, int(100/600.*HEIGHT)), (0, int(50/600.*HEIGHT)), (255, 255, 255), 0, (), (0, 0, 0), "files\\montserrat\\Montserrat-Black.otf")
    b = textbox.OutputBox(screen, "No Users Logged In", (WIDTH, int(50/600.*HEIGHT)), (0, int(175/600.*HEIGHT)), (255, 255, 255), 0, (), (0, 0, 0), "files\\montserrat\\Montserrat-Black.otf")
    c = textbox.OutputBox(screen, "Start", (int(770/800.*WIDTH-25/800.*WIDTH), int(580/600.*HEIGHT-490/600.*HEIGHT)), (int(25/800.*WIDTH), int(490/600.*HEIGHT)), (255, 255, 255), 0, (0, 0, 0), (0, 0, 0), "files\\montserrat\\Montserrat-Black.otf")

    prev_users = Server.update_login() #gets list of names
    print_names(screen, prev_users)#prints the name to the screen
    users = None
    mouse_loc = (0, 0)

    pygame.mixer.init()
    pygame.mixer.music.load(OST_DIR + "login.mp3")
    pygame.mixer.music.play(-1)
    trying = 0
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
        x, y = mouse_loc                                   #gets mouse location
        if 25/800.*WIDTH < x and x < 770/800.*WIDTH and y > 490/600.*HEIGHT and y < 580/600.*HEIGHT:    # if mouse above start button=
            screen.fill((35, 177, 76))
            for topstart in [x*int(WIDTH/10) for x in range(20)]:
                pygame.draw.line(screen, (176, 235, 48), (trying + topstart, -10), (-10, trying + topstart), int(0.0125*WIDTH))
            a.draw()
            b.draw()
            c.border_width = 6
            c.draw()
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)# set cursor to broken x
        else:
            screen.fill((35, 177, 76))
            for topstart in [x*int(WIDTH/10) for x in range(20)]:
                pygame.draw.line(screen, (176, 235, 48), (trying + topstart, -10), (-10, trying + topstart), int(0.0125*WIDTH))
            a.draw()
            b.draw()
            c.border_width = 0
            c.draw()
            pygame.mouse.set_cursor(*pygame.cursors.arrow)  # set cursor to an arrow

        users = Server.update_login()#gets updated list of names
        if users:
            if len(users) == 1:
                b.text = str(len(users)) + " User Logged In"
            else:
                b.text = str(len(users)) + " Users Logged In"
        else:
            b.text = "No Users Logged In"

        """update list"""
        if users != prev_users:
            for user in users:
                already_in = False
                for prev_user in prev_users:
                    if user == prev_user:
                        already_in = True
                if not already_in:
                    prev_users = [user] + prev_users

            for prev_user in prev_users:
                already_in = False
                for user in users:
                    if user == prev_user:
                        already_in = True
                if not already_in:
                    prev_users.remove(prev_user)

        print_names(screen, prev_users)

        pygame.display.flip()
        trying += 1
        if trying == WIDTH/10:
            trying = 0
        clock.tick(60)

    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    with open('quizes/test.json', 'rb') as qfile:
        quiz = json.load(qfile)

    #with open(IMAGES_DIR+"Example.jpg", 'rb') as img:
    #    quiz['Questions'][0]['photo'] = base64.b64encode(img.read())

    with open('quizes/test.json', 'wb') as qfile:
        json.dump(quiz, qfile, indent=4)

    pygame.mixer.music.fadeout(quiz['Questions'][0]['time to read']*1000)

    TotalQN = len(quiz['Questions'])
    first = True
    for q in quiz['Questions']:
        add_question(screen, q['time to read'], q['question'], [x.encode("utf-8") for x in q['answers']], q['correct answer'], q['photo'], q['image file type'], q['time to answer'], q['points'], first)
        first = False

    Server.end_game()
    names = Server.get_players()
    players = [x[1] for x in names]
    points = [x[0] for x in names]
    while len(players) < 3:
        players.append("None")
        points.append(0)
    Server.receive()
    exit_screen(screen, players, points)

    pygame.quit()
    time.sleep(0.2)
    exit()


def add_question(screen, timer, question, answers, correct_answer, photo, photype, qtime, points, first=False):
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

        if not first:
            done = score_board(screen, Server.get_players(), points)
            if done:
                return True

        done = load_timer(timer, screen, question)  # set timer for certain amount of time + print it
        if not done:
            Server.new_question(qtime, answers)  # sends a message to all client that a new question is now available
            done = load_question(screen, question, photo, answers, qtime)  # calls a function to print the question
            if not done:
                done = show_answer(screen, Server.results(correct_answer, points), correct_answer, question, photo)
            else:
                return True
        else:
            return True
        return False


def score_board(screen, players, next_round_points):
    image = pygame.image.load(IMAGES_DIR + "scoreboard\\scoreboard.png")
    image = resfix(image)


    # time
    start_time = time.time()

    #print players
    finish = False
    header = textbox.OutputBox(screen, "Scoreboard", (WIDTH, int(80/600.*HEIGHT)), (0, int(10/600.*HEIGHT)), (255, 255, 255), 0, (), (0, 0, 0), "files\\RosewoodStd-Regular.otf")
    users = []
    for i in range(5):
        if not i and players:
            users.append(textbox.OutputBox(screen, players[i][1] + "  -  " + str(players[i][0]) + " points", (int(700/800.*WIDTH), int(70/600.*HEIGHT)), (int(50/800.*WIDTH), int(120/600.*HEIGHT)), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), FONT_LIB + "ALGER.TTF"))
        elif i < len(players):
            users.append(textbox.OutputBox(screen, players[i][1] + "  -  " + str(players[i][0]) + " points", (int(700/800.*WIDTH), int(70/600.*HEIGHT)), (int(50/800.*WIDTH), int((70 * i + 20 + 120)/600.*HEIGHT)), (), 3, (0, 0, 0), (0, 0, 0), FONT_LIB + "ALGER.TTF"))
    under = textbox.OutputBox(screen, "Next round reward - " + str(next_round_points) + " points!", (int(650/800.*WIDTH), int(75/600.*HEIGHT)), (int(75/800.*WIDTH), int(525/600.*HEIGHT)), (163, 73, 163), 0, (), (255, 255, 255), "files\\montserrat\\Montserrat-Black.otf")
    while not finish:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
                return True
            if event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    exit()
                    return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    finish = True
                if event.key == pygame.K_p:
                    print pygame.mouse.get_pos()
        screen.blit(image, (0, 0))
        header.draw()
        for user in users:
            user.draw()
        under.draw()
        pygame.display.flip()
        Server.receive()
    return False


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
    question_text = textbox.OutputBox(screen, question, (WIDTH, int(70/600.*HEIGHT)), (0, 0), (255, 255, 255), 0, (), (0, 0, 0), "files\\montserrat\\Montserrat-Black.otf")

    # time
    start_time = time.time()

    time_passed = time.time() - start_time

    answer_boxes = []
    for y in range(4):
        answer_boxes.append(textbox.OutputBox(screen, text=answers[y], size=(int(335/800.*WIDTH), int(105/600.*HEIGHT)), place=(int(int(60/800.*WIDTH) + (WIDTH / 2) * (y % 2)), int(372/600.*HEIGHT) + int(120/600.*HEIGHT) * int(y / 2)),
                                              color=None, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf"))

    timerText = textbox.OutputBox(screen, text=str(qtime), size=(int((103-43-6)/800.*WIDTH), int((237-177)/600.*HEIGHT)), place=(int((43+3)/800.*WIDTH), int(177/600.*HEIGHT)),
                                              color=None, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")
    timerTextHeader = textbox.OutputBox(screen, text=" Seconds:", size=(int(142/800.*WIDTH), int((237-177+100)/600.*HEIGHT)), place=(0, int(177/600.*HEIGHT) - int((237-177+50)/600.*HEIGHT)),
                                              color=None, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf")

    answerText = textbox.OutputBox(screen, text=str(0), size=(int((753-693-6)/800.*WIDTH), int((235-175)/600.*HEIGHT)), place=(int((693+3)/800.*WIDTH), int(175/600.*HEIGHT)),
                                              color=None, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")
    answerTextHeader = textbox.OutputBox(screen, text="Answers: ", size=(int((800-664)/800.*WIDTH), int((235-175+100)/600.*HEIGHT)), place=(int(664/800.*WIDTH), int(175/600.*HEIGHT) - int((235-175+50)/600.*HEIGHT)),
                                              color=None, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf")

    pygame.mixer.music.load(OST_DIR + "question.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    answers_amount = 0
    while time_passed < qtime and answers_amount < len(users):
        events = pygame.event.get()
        answers_amount = Server.receive()
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
        pygame.draw.circle(screen, (201, 14, 163), (int(723 / 800. * WIDTH), int(206 / 600. * HEIGHT)), 30)
        pygame.draw.circle(screen, (201, 14, 163), (int(74 / 800. * WIDTH), int(206 / 600. * HEIGHT)), 30)
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

        # timer
        time_passed = time.time() - start_time
        timerText.text = str(int(qtime - time_passed))
        timerText.draw()
        timerTextHeader.draw()

        answerText.text = str(int(answers_amount)) if answers_amount is not None else "0"
        answerText.draw()
        answerTextHeader.draw()



        pygame.display.flip()
    pygame.mixer.music.stop()
    return False


def load_timer(num, screen, question,):
    global QuestioNumber, TotalQN
    QuestioNumber += 1
    first = time.time()
    last = time.time()
    current = time.time()
    count = 0
    question_text = textbox.OutputBox(screen, question, (WIDTH, int(70/600.*HEIGHT)), (0, int(312/600.*HEIGHT)), (255, 255, 255), 0, (), (0, 0, 0), "files\\montserrat\\Montserrat-Black.otf")
    question_id = textbox.OutputBox(screen, "Question " + str(QuestioNumber) + " out of " + str(TotalQN), (WIDTH, int(40/600.*HEIGHT)), (0, 0), (255, 255, 255), 0, (), (0, 0, 0), "files\\montserrat\\Montserrat-Black.otf")
    finish = False
    while current - first <= num + 0.4 and not finish:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                exit()
                return True
            if event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    exit()
                    return True
            #if event.type == pygame.KEYDOWN:
            #        if event.key == pygame.K_SPACE:
            #            finish = True
        current = time.time()
        if current - last > 0.05:
            hamster_img = pygame.image.load(IMAGES_DIR + "loading\\hamster\\Slide%s.png" % str(count/2 % 12 + 1))
            size = hamster_img.get_rect().size
            hamster_img = pygame.transform.scale(hamster_img, (int(size[0]/800.*WIDTH), int(size[1]/600.*HEIGHT)))

            image = pygame.image.load(IMAGES_DIR + "loading\wheel\\frame_%s_delay-0.04s.png" % str(19 - (count % 19)).zfill(2))
            size = image.get_rect().size
            image = pygame.transform.scale(image, (int(size[0]/800.*WIDTH), int(size[1]/600.*HEIGHT)))
            image.set_colorkey((0, 0, 0))

            screen.blit(BLACKSURFACE, (0, 0))
            x = 20 # width of a letter, change according to the font
            question_text.draw()
            screen.blit(hamster_img, (int(340/800.*WIDTH), int(50/600.*HEIGHT)))
            screen.blit(image, (int(300/800.*WIDTH), int(95/600.*HEIGHT)))
            bar = pygame.Surface((int((current - first)/num * WIDTH), int(60/600.*HEIGHT)))
            bar.fill((124, 0, 255))
            barop = pygame.Surface((WIDTH - int((current - first-0.3)/num * WIDTH) if WIDTH - int((current - first)/num * WIDTH) > 0 else 0, int(60/600.*HEIGHT)))
            barop.fill((188, 135, 243))
            screen.blit(barop, (int((current - first-0.3)/num * WIDTH), int(400/600.*HEIGHT)))
            screen.blit(bar, (0, int(400/600.*HEIGHT)))
            question_id.draw()
            pygame.display.flip()
            last = current
            count += 1
    return False


def show_answer(screen, res, correct_answer, question, photo):
    res_sum = max(res) if max(res) else 1
    rc = pygame.image.load(IMAGES_DIR + "main\\red_correct.png")
    rc = resfix(rc)
    bc = pygame.image.load(IMAGES_DIR + "main\\blue_correct.png")
    bc = resfix(bc)
    yc = pygame.image.load(IMAGES_DIR + "main\\orange_correct.png")
    yc = resfix(yc)
    gc = pygame.image.load(IMAGES_DIR + "main\\green_correct.png")
    gc = resfix(gc)
    inrc = pygame.image.load(IMAGES_DIR + "main\\red_incorrect.png")
    inrc = resfix(inrc)
    inbc = pygame.image.load(IMAGES_DIR + "main\\blue_incorrect.png")
    inbc = resfix(inbc)
    inyc = pygame.image.load(IMAGES_DIR + "main\\orange_incorrect.png")
    inyc = resfix(inyc)
    ingc = pygame.image.load(IMAGES_DIR + "main\\green_incorrect.png")
    ingc = resfix(ingc)
    red = inrc
    blue = inbc
    yellow = inyc
    green = ingc

    if correct_answer == 1:
        red = rc
    if correct_answer == 2:
        blue = bc
    if correct_answer == 3:
        yellow = yc
    if correct_answer == 4:
        green = gc

    addedimg = None
    if photo:
        addedimg = pygame.transform.scale(pygame.image.load("./files/temp.jpg"), (int((665-143)/800.*WIDTH), int((334-70)/600.*HEIGHT)))

    a = [3, 367, 403, 367, 3, 484, 403, 484]
    Rstartx, Rstarty, Bstartx, Bstarty, Ystartx, Ystarty, Gstartx, Gstarty = [int(a[x]/800.*WIDTH) if x % 2 == 0 else int(a[x]/600.*HEIGHT) for x in range(len(a))]
    questionFont = pygame.font.Font("files\\montserrat\\Montserrat-Black.otf", 50)
    question_text = textbox.OutputBox(screen, question, (WIDTH, int(70/600.*HEIGHT)), (0, 0), (255, 255, 255), 0, (), (0, 0, 0), "files\\montserrat\\Montserrat-Black.otf")

    Sx = 60.0/res_sum  # scale of moving according to the amount of answers in x
    Sy = 25.0/res_sum  # scale of moving according to the amount of answers in y

    c = 0

    finish = False
    pygame.mixer.music.set_volume(1)
    time.sleep(0.05)
    pygame.mixer.music.load(OST_DIR + "answers.mp3")
    pygame.mixer.music.play(1)
    last = time.time()
    while not finish:
        Server.receive()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
                return True
            if event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    exit()
                    return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False
        screen.fill(WHITE)
        pygame.draw.circle(screen, (201, 14, 163), (int(723 / 800. * WIDTH), int(206 / 600. * HEIGHT)), 30)
        pygame.draw.circle(screen, (201, 14, 163), (int(74 / 800. * WIDTH), int(206 / 600. * HEIGHT)), 30)
        width = int(395/800.*WIDTH)     #width of the rectengels
        height = int(111/600.*HEIGHT)    #height of the rectrngels
        if time.time() - last > 0.1:
            last = time.time()
            """Green rectengles"""
            Rrect1 = pygame.draw.polygon(screen, (11, 87, 4), [(Gstartx, Gstarty), (Gstartx + width, Gstarty),
                                                               (int(Gstartx + Sx*c * res[3] + width), int(Gstarty + Sy * c * res[3])),
                                                               (int(Gstartx + Sx * c * res[3]), int(Gstarty + Sy * c * res[3]))])
            Rrect2 = pygame.draw.polygon(screen, (29, 233, 12), [(Gstartx, Gstarty), (Gstartx, Gstarty + height),
                                                                 (int(Gstartx + Sx * c * res[3]), int(Gstarty + Sy * c * res[3] + height)),
                                                                 (int(Gstartx + Sx * c * res[3]), int(Gstarty + Sy * c * res[3]))])
            screen.blit(green, (Gstartx + res[3] * Sx * c, Gstarty + res[3] * Sy * c))
            amount = questionFont.render(str(int(res[3] * c)), False, WHITE)
            screen.blit(amount, (Gstartx + 130 + Sx * c * res[3], Gstarty + 40 + Sy * c * res[3]))

            """"Yellow rectengles"""
            Rrect1 = pygame.draw.polygon(screen, (128, 80, 0), [(Ystartx, Ystarty), (Ystartx + width, Ystarty),
                                                                (int(Ystartx + Sx * c * res[2] + width), int(Ystarty + Sy * c * res[2])),
                                                                (int(Ystartx + Sx * c * res[2]), int(Ystarty + Sy * c * res[2]))])
            Rrect2 = pygame.draw.polygon(screen, (254, 172, 35), [(Ystartx, Ystarty), (Ystartx, Ystarty + height),
                                                                  (int(Ystartx + Sx * c * res[2]), int(Ystarty + Sy * c * res[2] + height)),
                                                                  (int(Ystartx + Sx * c * res[2]), int(Ystarty + Sy * c * res[2]))])
            screen.blit(yellow, (Ystartx + res[2] * Sx * c, Ystarty + res[2] * Sy * c))
            amount = questionFont.render(str(int(res[2] * c)), False, WHITE)
            screen.blit(amount, (Ystartx + 130 + Sx * c * res[2], Ystarty + 40 + Sy * c * res[2]))

            """Blue rectengles"""
            Rrect1 = pygame.draw.polygon(screen, (1, 23, 75), [(Bstartx, Bstarty), (Bstartx + width, Bstarty),
                                                               (int(Bstartx + Sx * c * res[1] + width), int(Bstarty + Sy * c * res[1])),
                                                               (int(Bstartx + Sx * c * res[1]), int(Bstarty + Sy * c * res[1]))])
            Rrect2 = pygame.draw.polygon(screen, (54, 114, 252), [(Bstartx, Bstarty), (Bstartx, Bstarty + height),
                                                                  (int(Bstartx + Sx * c * res[1]), int(Bstarty + Sy * c * res[1] + height)),
                                                                  (int(Bstartx + Sx * c * res[1]), int(Bstarty + Sy * c * res[1]))])
            screen.blit(blue, (Bstartx + res[1] * Sx * c, Bstarty + res[1] * Sy * c))
            amount = questionFont.render(str(int(res[1] * c)), False, WHITE)
            screen.blit(amount, (Bstartx + 130 + Sx * c * res[1], Bstarty + 40 + Sy * c * res[1]))

            """red rectengles"""
            Rrect1 = pygame.draw.polygon(screen, (106, 3, 0), [(Rstartx, Rstarty), (Rstartx + width, Rstarty),
                                                               (int(Rstartx + Sx * c * res[0] + width), int(Rstarty + Sy * c * res[0])),
                                                               (int(Rstartx + Sx * c * res[0]), int(Rstarty + Sy * c * res[0]))])
            Rrect2 = pygame.draw.polygon(screen, (255, 44, 38), [(Rstartx, Rstarty), (Rstartx, Rstarty + height),
                                                                 (int(Rstartx + Sx * c * res[0]), int(Rstarty + Sy * c * res[0] + height)),
                                                                 (int(Rstartx + Sx * c * res[0]), int(Rstarty + Sy * c * res[0]))])
            screen.blit(red, (Rstartx + res[0] * Sx * c, Rstarty + res[0] * Sy * c))
            amount = questionFont.render(str(int(res[0] * c)), False, WHITE)
            screen.blit(amount, (Rstartx + 130 + Sx * c * res[0], Rstarty + 40 + Sy * c * res[0]))
            question_text.draw()
            if addedimg:
                screen.blit(addedimg, (int(143/800.*WIDTH), int(75/600.*HEIGHT)))
            else:
                textbox.OutputBox(screen, text=" KABOOT! ", size=(int((665-143)/800.*WIDTH), int((334-75)/600.*HEIGHT)), place=(int(143/800.*WIDTH), int(75/600.*HEIGHT)),
                                          color=(201, 14, 163), text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf").draw()


            pygame.display.flip()

            c = c + 0.1 if c + 0.1 <= 1 else 1

    return False


def exit_screen(screen, names, points):



    sizes = [85, 85, 85]
    for i in range(3):
        answerFont = pygame.font.Font(None, sizes[i])
        while answerFont.size(names[i])[0] > int(132/800.*WIDTH):
            sizes[i] -= 1
            answerFont = pygame.font.Font(None, sizes[i])

    pygame.mixer.music.load(OST_DIR + "winners.mp3")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)

    gif = 0
    speed = 1
    sub = False
    finish = False
    la_finito = False
    up = 0
    last = time.time()
    start = last
    final = [350, 386, 419]
    podioms = [400, 327, 241]
    while not finish:
        Server.receive()
        current = time.time()
        last = current
        screen.fill((87, 37, 194))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.mixer.music.fadeout(gif*100)
                finish = True
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if gif > 56:
                        pygame.mixer.music.fadeout(gif*100)
                        la_finito = True


        image = pygame.image.load(IMAGES_DIR + "win_background\\frame_%s_delay-0.04s.png" % str(gif % 178).zfill(3))
        image = resfix(image)
        screen.blit(image, (0, up))
        speed += 1

        if not la_finito:
            if current - start >= 8:
                podioms[0] = podioms[0] - 4 if podioms[0] - 4 >= 0 else 0
                podioms[2] = podioms[2] - 4 if podioms[2] - 4 >= 0 else 0
                podioms[1] = podioms[1] - 4 if podioms[1] - 4 >= 0 else 0
        else:
                podioms = [x + (178 - gif)/7 for x in podioms]


        image = pygame.image.load(IMAGES_DIR + "winners_stand\\Slide1.png")
        image = pygame.transform.scale(image, (WIDTH/5, int(HEIGHT*1.3)))
        screen.blit(image, (int((800/2 - 74)/800.*WIDTH), int((final[0] + podioms[0])/600.*HEIGHT)))
        textbox.OutputBox(screen, str(points[0]) + " points!", (WIDTH/5-WIDTH/25, int(45/600.*HEIGHT)), (int((800/2 - 74)/800.*WIDTH+WIDTH/50), int((final[0] + podioms[0] + 130)/600.*HEIGHT)), None, 0, None, (255, 255, 255), "files\\montserrat\\Montserrat-Black.otf").draw()
        textbox.OutputBox(screen, names[0], (WIDTH/5-WIDTH/25, int(80/600.*HEIGHT)), (int((800/2 - 74)/800.*WIDTH+WIDTH/50), int((final[0] + podioms[0])/600.*HEIGHT)), None, 0, None, (255, 255, 255), "files\\montserrat\\Montserrat-Black.otf").draw()


        image = pygame.image.load(IMAGES_DIR + "winners_stand\\Slide2.png")
        image = pygame.transform.scale(image, (WIDTH/5, int(HEIGHT*1.3)))
        screen.blit(image, (int((800/2 - 74*4)/800.*WIDTH), int((final[1] + podioms[1])/600.*HEIGHT)))
        textbox.OutputBox(screen, str(points[1]) + " points!", (WIDTH/5-WIDTH/25, int(45/600.*HEIGHT)), (int((800/2 - 74*4)/800.*WIDTH+WIDTH/50), int((final[1] + podioms[1] + 130)/600.*HEIGHT)), None, 0, None, (255, 255, 255), "files\\montserrat\\Montserrat-Black.otf").draw()
        textbox.OutputBox(screen, names[1], (WIDTH/5-WIDTH/25, int(80/600.*HEIGHT)), (int((800/2 - 74*4)/800.*WIDTH+WIDTH/50), int((final[1] + podioms[1])/600.*HEIGHT)), None, 0, None, (255, 255, 255), "files\\montserrat\\Montserrat-Black.otf").draw()

        image = pygame.image.load(IMAGES_DIR + "winners_stand\\Slide3.png")
        image = pygame.transform.scale(image, (WIDTH/5, int(HEIGHT*1.3)))
        screen.blit(image, (int((800/2 + 74*2)/800.*WIDTH), int((final[2] + podioms[2])/600.*HEIGHT)))
        textbox.OutputBox(screen, str(points[2]) + " points!", (WIDTH/5-WIDTH/25, int(45/600.*HEIGHT)), (int((800/2 + 74*2)/800.*WIDTH+WIDTH/50), int((final[2] + podioms[2] + 130)/600.*HEIGHT)), None, 0, None, (255, 255, 255), "files\\montserrat\\Montserrat-Black.otf").draw()
        textbox.OutputBox(screen, names[2], (WIDTH/5-WIDTH/25, int(80/600.*HEIGHT)), (int((800/2 + 74*2)/800.*WIDTH+WIDTH/50), int((final[2] + podioms[2])/600.*HEIGHT)), None, 0, None, (255, 255, 255), "files\\montserrat\\Montserrat-Black.otf").draw()

        if la_finito:
            if gif <= 56:
                if up > -HEIGHT+HEIGHT/8:
                    up -= 10
                else:
                    finish = True
            gif -= 1
        elif gif == 177:
            sub = True
            gif -= 1
        elif gif > 38:
            if sub and gif > 94:
                gif -= 1
            else:
                sub = False
                gif += 1
        else:
            if gif < 38 or time.time() - start >= 7:
                if speed % 3 == 0:
                    gif += 1

        pygame.display.flip()
        clock.tick(24)


def print_names(screen, names):
    counter = 0
    for y in range(3):
        for x in range(5):
            if counter < len(names):
                textbox.OutputBox(screen=screen, text=names[counter], size=(WIDTH/6, HEIGHT/10), place=(5 + x * (WIDTH / 5), int(245/600.*HEIGHT) + HEIGHT/8*y), color=WHITE, border_width=2, border_color=BLACK, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf").draw()
                counter += 1

    if False:
        if len(names[x] ) > 3:
            largeText = pygame.font.Font(None, int(WIDTH/4/len(names[x])) - int(30/len(names[x])) + 5)
            name_text = largeText.render(names[x], False, BLACK)#print the name
            screen.blit(name_text, (x % 4 * (WIDTH / 4) + 20, int(245/600.*HEIGHT) + int(x / 4) * 60))
        else:
            largeText = pygame.font.Font(None, 60)
            name_text = largeText.render(names[x], False, BLACK)  # print
            screen.blit(name_text, (x % 4 * (WIDTH / 4), int(230/600.*HEIGHT) + int(x / 4) * 60))



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
    pygame.draw.circle(screen, (0,0,0), pos, 30, width)


def resfix(image):
    size = image.get_rect().size
    return pygame.transform.scale(image, (int(size[0]/800.*WIDTH), int(size[1]/600.*HEIGHT)))


class Button:
    def __init__(self, width, height, color, location):
        self.drawn = False
        self.height = height
        self.width = width
        self.color = color
        self.location = location
        self.background = pygame.Surface((width, height))
        self.background.fill(color)
        self.items = {}
        self.screen = None

    def Draw(self, screen):
        self.screen = screen
        for item in self.items.keys():
            self.background.blit(item, self.items[item])
        screen.blit(self.background, self.location)
        pygame.display.flip()
        self.drawn = True


    def add_item(self, item, location):
        self.items[item] = location
        if self.drawn:
            item.fill(BLUE)
            self.background.blit(item, location)
            self.screen.blit(self.background, self.location)
            pygame.display.flip()


main()
