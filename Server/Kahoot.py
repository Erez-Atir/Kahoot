import pygame
from pygame.locals import *
import time
import random
import os
import sys
sys.path.insert(0, os.getcwd()+'/files')
import Server
sys.dont_write_bytecode = True

PLAYERSSCORE = {} #""""dictionary, saves the points of each player"""
FONT_LIB = pygame.font.match_font('bitstreamverasans')[0:-10]#finds the fony libary path
IMAGES_DIR = os.getcwd() + "\\images\\" #saves the path to the images libary
OST_DIR = os.getcwd() + "\\audio\\"

"""defauly pygame settings"""
MouseButtonDown = 6
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
TCHELET = (150, 150, 255)
MouseMotion = 4

"""height and width of the screen"""
HEIGHT = 600
WIDTH = 800

"""vars for un used libary update_login"""
LASTUPDATECALL = time.time()
NAMELIST = []
RANDO = 1

"""white surface in the size of the screen"""
BLACKSURFACE = pygame.Surface((WIDTH, HEIGHT))
BLACKSURFACE.fill(WHITE)


def main():
    exit = False                                     #"""the playes exited the game?"""
    start_game = False                               # the game has started?
    pygame.init()                                    # initiate pygames

    screen = pygame.display.set_mode((WIDTH, HEIGHT))#set screen wid =800, hieght =600
    pygame.display.flip()
    pygame.font.init()
    if os.path.exists(IMAGES_DIR + "login\\log_screen.png"): #if path to an image exists
        log_screen = pygame.image.load(IMAGES_DIR + "login\\log_screen.png")#load image
        screen.blit(log_screen, (0,0))
        pygame.display.flip()
    else:                                             #else
        log_screen = pygame.Surface((WIDTH, HEIGHT))  #load nothing
    if os.path.exists(IMAGES_DIR + "login\\log_screen_start_selected.png"): #if path to an image exists
        log_screen_start_selcted = pygame.image.load(IMAGES_DIR + "login\\log_screen_start_selected.png") #load image
    else:
        log_screen_start_selcted = pygame.Surface((WIDTH, HEIGHT)) #white surface incase path doesn't exists
    largeText = pygame.font.Font('freesansbold.ttf', 50)#set a font

    prev_users = Server.update_login() #gets list of names
    print_names(screen, prev_users)#prints the name to the screen
    users = None
    mouse_loc = (0, 0)

    pygame.mixer.init()
    pygame.mixer.music.load(OST_DIR + "login.mp3")
    pygame.mixer.music.play(-1)
    while not start_game and not exit: #while game was not exited and game is still at the log in part
        events = pygame.event.get()
        """checks events, user input"""
        for event in events:#checks for events including:
            if event.type == MouseMotion:#mouse hovering above the start button
                x, y = event.pos
                mouse_loc = event.pos

            if event.type == pygame.QUIT:#user presses the X
                exit = True
            if event.type == MouseButtonDown:#player clicks the screen(should be only button)
                x, y = event.pos
                if 25 < x and x < 770 and y > 490 and y < 580:  # if mouse above start button
                    pygame.mixer.music.fadeout(5000)
                    start_game = True
        """"load screen"""
        x, y = mouse_loc                                   #gets mouse location
        if 25 < x and x < 770 and y > 490 and y < 580:     # if mouse above start button
            screen.blit(log_screen_start_selcted, (0, 0))  # fill the screen with bold "start" image
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)# set cursor to broken x
        else:
            screen.blit(log_screen, (0, 0))  # fill screen with regaular log screen
            pygame.mouse.set_cursor(*pygame.cursors.arrow)  # set cursor to an arrow

        users = Server.update_login()#gets updated list of names

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
        print_names(screen, prev_users) #print the users

    if not exit:
        exit = add_question(screen, 6, "The correct answer is number 2", ["1", "2", "3", "4"], 2, None, 10, 1000)
    if not exit:
            exit = add_question(screen, 5, "Who shot the sheriff?", ["I shot the sheriff", "but I did not shoot the deputy", "It was santa!", "Chuck Norris did it!"], 1, None, 10, 800)
    if not exit:
        exit = add_question(screen, 5, "Is this the real life?", ["It's just a fantasy.", "Caught in a landslide", "No escape from reality", "Open your eyes"], 4, None, 10, 800)

    if not exit:
        Server.end_game()
        for buffer in xrange(100):
            Server.receive()
        players = Server.get_players().keys()
        while len(players) < 3:
            players.append("NO ONE")
        exit_screen(screen, players)
    pygame.quit()


def add_question(screen, timer, question, answers, correct_answer, photo, qtime, points):
        """
        function that adds a question to the game
        :param screen: gets the screen obj to print on
        :param timer:  gets the amount of time before question
        :param question: gets the question (no longer than 40 letters)
        :param answers:  gets the possible answers
        :param correct_answer:  gets the number of the correct answer
        :param photo: gets a photo that's relevant to the question
        :param qtime: gets time to answer the question
        :param points: gets the maximum points recived py this question
        :return: Was the server closed
        """

        exit = load_timer(timer, screen, question)#set timmer for certain amount of time + print it
        if not exit:
            Server.new_question(qtime) # sends a message to all client that a new question is now available
            exit = load_question(screen, question, photo, answers, qtime) #"""calls a function to print the question"""
            if not exit:
                exit = show_answer(screen, Server.results(correct_answer, points), correct_answer, question)
                if exit:
                    return True
            else:
                return True
        else:
            return True
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


    """image"""
    if photo:
        image = pygame.image.load(IMAGES_DIR + "main\\questions.png")
    else:
        image = pygame.image.load(IMAGES_DIR + "main\\questions_no_image.png")

    """question"""
    questionFont = timerFont = pygame.font.Font(get_font("bauhaus93"), 50)
    questionText = questionFont.render(question, False, BLACK)
    x = 20  # widtgh of a letter, change according to font so the question will be in the middle of the screen

    """time"""
    start_time = time.time()

    time_passed = time.time() - start_time

    pygame.mixer.music.load(OST_DIR + "question.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    while time_passed < qtime:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.mixer.music.stop()
                return True
        screen.blit(image, (0, 0))
        """question"""
        screen.blit(questionText, (int((WIDTH / x - len(question)) / 2 * x), 30))
        """answers"""
        for y in range(4):
            answerFont = pygame.font.Font(get_font("bauhaus93"), int(50 - (len(answers[y])/1.4)))
            answerText = answerFont.render(answers[y], False, WHITE)
            screen.blit(answerText, (int(70 + (WIDTH / 2) * (y % 2)), 405 + 120 * int(y / 2)))

        """timer"""
        time_passed = time.time() - start_time
        timerText = questionFont.render(str(int(qtime - time_passed)), False, WHITE)
        if len(str(int(qtime - time_passed))) == 2:
            screen.blit(timerText, (55, 192))
            screen.blit(timerText, (705, 192))
        else:
            screen.blit(timerText, (63, 192))
            screen.blit(timerText, (713, 192))
        pygame.display.flip()
        Server.receive()
    pygame.mixer.music.stop()
    return False


def load_timer(num, screen, question):
    first = time.time()
    last = time.time()
    #already_rotated = 0
    questionFont = pygame.font.Font(get_font("bauhaus93"), 50)
    questionText = questionFont.render(question, False, BLACK)
    current = time.time()
    count = 0
    while current - first <= num + 0.4:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                return True
        current = time.time()
        if current - last > 0.05:
            hamster_img = pygame.image.load(IMAGES_DIR + "loading\\hamster\\Slide%s.png" % str(count/2 % 12 + 1))

            image = pygame.image.load(IMAGES_DIR + "loading\wheel\\frame_%s_delay-0.04s.png" % str(19 - (count % 19)).zfill(2))
            image.set_colorkey((0, 0, 0))

            screen.blit(BLACKSURFACE, (0, 0))
            x = 20 # width of a letter, change according to the font
            screen.blit(questionText, (int((WIDTH/x - len(question))/2 * x), 312))
            screen.blit(hamster_img, (350, 50))
            screen.blit(image, (300, 95))
            bar = pygame.Surface((int((current - first)/num * WIDTH), 60))
            bar.fill((124, 0, 255))
            barop = pygame.Surface((WIDTH - int((current - first-0.3)/num * WIDTH) if WIDTH - int((current - first)/num * WIDTH) > 0 else 0, 60))
            barop.fill((188, 135, 243))
            screen.blit(barop, (int((current - first-0.3)/num * WIDTH), 400))
            screen.blit(bar, (0, 400))
            pygame.display.flip()
            last = current
            count += 1
    return False


def show_answer(screen, res, correct_answer, question):

    bo = True
    rc = pygame.image.load(IMAGES_DIR + "main\\red_correct.png")          #loads all of the photoes containning:
    bc = pygame.image.load(IMAGES_DIR + "main\\blue_correct.png")         #Yellow correct and incorrect ect.
    yc = pygame.image.load(IMAGES_DIR + "main\\orange_correct.png")
    gc = pygame.image.load(IMAGES_DIR + "main\\green_correct.png")
    inrc = pygame.image.load(IMAGES_DIR + "main\\red_incorrect.png")
    inbc = pygame.image.load(IMAGES_DIR + "main\\blue_incorrect.png")
    inyc = pygame.image.load(IMAGES_DIR + "main\\orange_incorrect.png")
    ingc = pygame.image.load(IMAGES_DIR + "main\\green_incorrect.png")
    #if the color is correct load the correct form of him and the incorrect form of the rest
    starttime = time.time()
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
    basic_form = pygame.image.load(IMAGES_DIR + "main\\basic_result_form.png")

    Rstartx, Rstarty, Bstartx, Bstarty, Ystartx, Ystarty, Gstartx, Gstarty = 3, 367, 403, 368, 3, 484, 403, 484
    questionFont = timerFont = pygame.font.Font(get_font("bauhaus93"), 50)
    questionText = questionFont.render(question, False, BLACK)

    exit = False

    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.load(OST_DIR + "answers.mp3")
    pygame.mixer.music.play(-1)
    time.sleep(0.5)
    pygame.mixer.music.fadeout(600)
    while not exit:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False
        screen.blit(basic_form, (0,0))
        x = 20
        Sx = 3 # scale of moving according to the amount of answers in x
        Sy = 2 # scale of moving according to the amount of answers in y

        width = 395     #width of the rectengels
        height = 111    #height of the rectrngels

        """Green rectengles"""
        Rrect1 = pygame.draw.polygon(screen, (11, 87, 4), [(Gstartx, Gstarty), (Gstartx + width, Gstarty),
                                                           (Gstartx + Sx * res[3] + width, Gstarty + Sy * res[3]),
                                                           (Gstartx + Sx * res[3], Gstarty + Sy * res[3])])
        Rrect2 = pygame.draw.polygon(screen, (29, 233, 12), [(Gstartx, Gstarty), (Gstartx, Gstarty + height),
                                                             (Gstartx + Sx * res[3], Gstarty + Sy * res[3] + height),
                                                             (Gstartx + Sx * res[3], Gstarty + Sy * res[3])])
        screen.blit(green, (Gstartx + res[3] * Sx, Gstarty + res[3] * Sy))
        amount = questionFont.render(str(res[3]), False, WHITE)
        screen.blit(amount, (Gstartx + 130 + Sx * res[3], Gstarty + 40 + Sy * res[3]))

        """"Yellow rectengles"""
        Rrect1 = pygame.draw.polygon(screen, (128, 80, 0), [(Ystartx, Ystarty), (Ystartx + width, Ystarty),
                                                            (Ystartx + Sx * res[2] + width, Ystarty + Sy * res[2]),
                                                            (Ystartx + Sx * res[2], Ystarty + Sy * res[2])])
        Rrect2 = pygame.draw.polygon(screen, (254, 172, 35), [(Ystartx, Ystarty), (Ystartx, Ystarty + height),
                                                              (Ystartx + Sx * res[2], Ystarty + Sy * res[2] + height),
                                                              (Ystartx + Sx * res[2], Ystarty + Sy * res[2])])
        screen.blit(yellow, (Ystartx + res[2] * Sx, Ystarty + res[2] * Sy))
        amount = questionFont.render(str(res[2]), False, WHITE)
        screen.blit(amount, (Ystartx + 130 + Sx * res[2], Ystarty + 40 + Sy * res[2]))

        """Blue rectengles"""
        Rrect1 = pygame.draw.polygon(screen, (1, 23, 75), [(Bstartx, Bstarty), (Bstartx + width, Bstarty),
                                                           (Bstartx + Sx * res[1] + width, Bstarty + Sy * res[1]),
                                                           (Bstartx + Sx * res[1], Bstarty + Sy * res[1])])
        Rrect2 = pygame.draw.polygon(screen, (54, 114, 252), [(Bstartx, Bstarty), (Bstartx, Bstarty + height),
                                                              (Bstartx + Sx * res[1], Bstarty + Sy * res[1] + height),
                                                              (Bstartx + Sx * res[1], Bstarty + Sy * res[1])])
        screen.blit(blue, (Bstartx + res[1] * Sx, Bstarty + res[1] * Sy))
        amount = questionFont.render(str(res[1]), False, WHITE)
        screen.blit(amount, (Bstartx + 130 + Sx * res[1], Bstarty + 40 + Sy * res[1]))

        """red rectengles"""
        Rrect1 = pygame.draw.polygon(screen, (106, 3, 0), [(Rstartx, Rstarty), (Rstartx + width, Rstarty),
                                                           (Rstartx + Sx * res[0] + width, Rstarty + Sy * res[0]),
                                                           (Rstartx + Sx * res[0], Rstarty + Sy * res[0]) ])
        Rrect2 = pygame.draw.polygon(screen, (255, 44, 38), [(Rstartx, Rstarty), (Rstartx, Rstarty + height),
                                                             (Rstartx + Sx * res[0], Rstarty + Sy * res[0] + height),
                                                             (Rstartx + Sx * res[0], Rstarty + Sy * res[0])])
        screen.blit(red, (Rstartx + res[0] * Sx, Rstarty + res[0] * Sy))
        amount = questionFont.render(str(res[0]), False, WHITE)
        screen.blit(amount, (Rstartx + 130 + Sx * res[0], Rstarty + 40 + Sy * res[0]))





        screen.blit(questionText, (int((WIDTH / x - len(question)) / 2 * x), 30))







        """for y in range(4):
            answerFont = pygame.font.Font(get_font("bauhaus93"), int(50 - (len(answers[y])/1.4)))
            answerText = answerFont.render(answers[y], False, WHITE)
            screen.blit(answerText, (int(70 + (WIDTH / 2) * (y % 2)), 405 + 120 * int(y / 2)))"""
        pygame.display.flip()
        if bo:
            starttime = time.time()
            bo = False
    return False


def exit_screen(screen, names):

    clock = pygame.time.Clock()

    sizes = [400, 400, 400]
    for i in range(3):
        answerFont = pygame.font.Font(get_font("bauhaus93"), sizes[i])
        while answerFont.size(names[i])[0] > 132:
            sizes[i] -= 1
            answerFont = pygame.font.Font(get_font("bauhaus93"), sizes[i])

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
        if current - last > 0.11:
            last = current
            screen.fill((87, 37, 194))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.fadeout(gif*100)
                    la_finito = True
            image = pygame.image.load(IMAGES_DIR + "win_background\\frame_%s_delay-0.04s.png" % str(gif % 178).zfill(3))
            screen.blit(image, (0, up))
            speed += 1

            if pygame.key.get_pressed()[K_SPACE]:
                print gif
                print pygame.mouse.get_pos()
                print

            if not la_finito:
                if current - start >= 7:
                    podioms[0] = podioms[0] - 6 if podioms[0] - 6 >= 0 else 0
                if current - start >= 14.5:
                    podioms[1] = podioms[1] - 6 if podioms[1] - 6 >= 0 else 0
                if current - start >= 23:
                    podioms[2] = podioms[2] - 6 if podioms[2] - 6 >= 0 else 0
            else:
                    podioms = [x + (178 - gif)/20 for x in podioms]


            answerFont = pygame.font.Font(get_font("bauhaus93"), sizes[0])
            answerText = answerFont.render(names[0], False, WHITE, TCHELET)
            textW, textH = answerFont.size(names[0])
            screen.blit(answerText, (WIDTH/2 - textW/2, final[0] + podioms[0] - textH))
            image = pygame.image.load(IMAGES_DIR + "winners_stand\\Slide1.png")
            image.set_colorkey(BLACK)
            screen.blit(image, (WIDTH/2 - 74, final[0] + podioms[0]))

            answerFont = pygame.font.Font(get_font("bauhaus93"), sizes[1])
            answerText = answerFont.render(names[1], False, WHITE, TCHELET)
            textW, textH = answerFont.size(names[1])
            screen.blit(answerText, (WIDTH/2 - 74*3 - textW/2, final[1] + podioms[1] - textH))
            image = pygame.image.load(IMAGES_DIR + "winners_stand\\Slide2.png")
            image.set_colorkey(BLACK)
            screen.blit(image, (WIDTH/2 - 74*4, final[1] + podioms[1]))

            answerFont = pygame.font.Font(get_font("bauhaus93"), sizes[2])
            answerText = answerFont.render(names[2], False, WHITE, TCHELET)
            textW, textH = answerFont.size(names[2])
            screen.blit(answerText, (WIDTH/2 + 74*3 - textW/2, final[2] + podioms[2] - textH))
            image = pygame.image.load(IMAGES_DIR + "winners_stand\\Slide3.png")
            image.set_colorkey(BLACK)
            screen.blit(image, (WIDTH/2 + 74*2, final[2] + podioms[2]))

            if la_finito:
                if gif <= 56:
                    if up > -HEIGHT+100:
                        up -= 10
                    else:
                        finish = True
                gif -= 1
            elif gif == 177:
                sub = True
                gif -= 1
            elif gif > 29:
                if sub and gif > 94:
                    gif -= 1
                else:
                    sub = False
                    gif += 1
            elif speed % 2 == 0:
                gif += 1

            pygame.display.flip()
            clock.tick(60)


def print_names(screen, names):
    for x in range(min(16, len(names))):#if there is place on the screen
        if len(names[x] ) > 3:
            largeText = pygame.font.Font(get_font("bauhaus93"), int(WIDTH/4/len(names[x])) - int(30/len(names[x])) + 5)
            name_text = largeText.render(names[x], False, BLACK)#print the name
            screen.blit(name_text, (x % 4 * (WIDTH / 4) + 20, 245 + int(x / 4) * 60))
        else:
            largeText = pygame.font.Font(get_font("bauhaus93"), 60)
            name_text = largeText.render(names[x], False, BLACK)  # prin
            screen.blit(name_text, (x % 4 * (WIDTH / 4), 230 + int(x / 4) * 60))

    pygame.display.flip()


def get_font(name):
    FONT_LIB + name + ".ttf"


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