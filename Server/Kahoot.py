import pygame
from pygame.locals import *
import time
import os
from files import Server
from files import textbox

PLAYERSSCORE = {} #""""dictionary, saves the points of each player"""
FONT_LIB = pygame.font.match_font('bitstreamverasans')[0:-10] + "\\" #finds the fony libary path
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
    done = False                                     #"""the playes exited the game?"""
    start_game = False                               # the game has started?
    pygame.init()                                    # initiate pygames

    #screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)  # full screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # set screen wid =800, hieght =600

    pygame.display.set_caption("Kaboot")
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
    while not start_game and not done: #while game was not exited and game is still at the log in part
        events = pygame.event.get()
        """checks events, user input"""
        for event in events:#checks for events including:
            if event.type == MouseMotion:#mouse hovering above the start button
                x, y = event.pos
                mouse_loc = event.pos

            if event.type == pygame.QUIT:#user presses the X
                done = True
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
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    Server.ServerDitection.finish = True
    if not done:
        done = add_question(screen, 5, "Is your GUI working?", ["Yes!", "No!", "I can't answer because\nit has already crashed", "Who is GUI?"], 1, None, 40, 100, True)
    if not done:
        done = add_question(screen, 7, "What can you do in a Pygame program?", ["Display photos", "Play sounds", "Create moving sprites", "All of the answers are correct"], 4, None, 40, 1000, True)
    if not done:
            done = add_question(screen, 10, "Which of the following did not appear in the presentation?", ["Fill", "David Ben Gurion", "Binyamin Netanyahu", "Arnold Schwarzenegger"], 3, None, 40, 200)
    if not done:
        done = add_question(screen, 5, "Why would someone use a sprite?", ["To draw a Square", "To color the screen", "To handle large numbers\nof objects on screen", "To display an image on screen"], 3, None, 40, 1000)
    if not done:
            done = add_question(screen, 9, "How much sprites was in the sprite group in our presentation?", ["3", "6", "10", "7"], 2, None, 40, 300)
    if not done:
        done = add_question(screen, 5, "What function allows us to color a surface?", ["fill()", "paint()", "leaf()", "color()"], 1, None, 40, 1000)
    if not done:
        done = add_question(screen, 8, "What color format do Pygame functions relieve?", ["BGR", "RGB", "BMP", "LLS"], 2, None, 40, 1000, True)
    if not done:
            done = add_question(screen, 10, "Did you have fun making your own GUI as a client for our kaboot?", ["YES!!! So much fun!", "No! I hated it!", "hmmmmf, it was ok", "is GUI a friend of Fill?"], 1, None, 40, 50)
    if not done:
        Server.end_game()
        for buffer in xrange(100):
            Server.receive()
        names = Server.get_players()
        players = names.keys()
        points = names.values()
        while len(players) < 3:
            players.append("None")
            points.append(0)
        exit_screen(screen, players, points)

    pygame.quit()
    time.sleep(0.2)
    exit()


def add_question(screen, timer, question, answers, correct_answer, photo, qtime, points, first=False):
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

        if not first:
            done = score_board(screen, Server.get_players(), points)
            if done:
                return True

        done = load_timer(timer, screen, question)#set timmer for certain amount of time + print it
        if not done:
            Server.new_question(qtime) # sends a message to all client that a new question is now available
            done = load_question(screen, question, photo, answers, qtime) #"""calls a function to print the question"""
            if not done:
                done = show_answer(screen, Server.results(correct_answer, points), correct_answer, question)
            else:
                return True
        else:
            return True
        return False


def score_board(screen, players, next_round_points):
    image = pygame.image.load(IMAGES_DIR + "scoreboard\\scoreboard.png")


    # time
    start_time = time.time()

    time_passed = time.time() - start_time

    finish = False
    header = textbox.OutputBox(screen, "Scoreboard", (800, 90), (0, 0), (255, 255, 255), 0, (), (0, 0, 0), "files\\RosewoodStd-Regular.otf")
    users = []
    for i in range(5):
        if not i and players:
            users.append(textbox.OutputBox(screen, players.keys()[i] + "  -  " + str(players.values()[i]) + " points", (700, 70), (50, 120), (255, 255, 255), 3, (0, 0, 0), (0, 0, 0), FONT_LIB + "ALGER.TTF"))
        elif i < len(players.keys()):
            users.append(textbox.OutputBox(screen, players.keys()[i] + "  -  " + str(players.values()[i]) + " points", (700, 70), (50, 70 * i + 20 + 120), (), 3, (0, 0, 0), (0, 0, 0), FONT_LIB + "ALGER.TTF"))
    under = textbox.OutputBox(screen, "Next round reward - " + str(next_round_points) + " points!", (650, 75), (75, 525), (163, 73, 163), 0, (), (255, 255, 255), get_font("BAUHS93"))
    while not finish:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
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


    # image
    if photo:
        image = pygame.image.load(IMAGES_DIR + "main\\questions.png")
    else:
        image = pygame.image.load(IMAGES_DIR + "main\\questions_no_image.png")

    # question
    question_text = textbox.OutputBox(screen, question, (800, 70), (0, 30), (255, 255, 255), 0, (), (0, 0, 0), get_font("BAUHS93"))
    x = 20  # widtgh of a letter, change according to font so the question will be in the middle of the screen

    # time
    start_time = time.time()

    time_passed = time.time() - start_time

    answer_boxes = []
    for y in range(4):
        answer_boxes.append(textbox.OutputBox(screen, text=answers[y], size=(335, 105), place=(int(60 + (WIDTH / 2) * (y % 2)), 372 + 120 * int(y / 2)),
                                              color=None, text_color=WHITE, font=get_font("BAUHS93")))

    pygame.mixer.music.load(OST_DIR + "question.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    while time_passed < qtime:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return True
        screen.blit(image, (0, 0))

        # question
        question_text.draw()

        # answers
        for answer in answer_boxes:
            answer.draw()

        # timer
        time_passed = time.time() - start_time
        timerText = pygame.font.Font(None, 50).render(str(int(qtime - time_passed)), False, WHITE)
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
    current = time.time()
    count = 0
    question_text = textbox.OutputBox(screen, question, (800, 70), (0, 312), (255, 255, 255), 0, (), (0, 0, 0), get_font("BAUHS93"))
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
            question_text.draw()
            screen.blit(hamster_img, (340, 50))
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
    res_sum = max(res) if max(res) else 1
    rc = pygame.image.load(IMAGES_DIR + "main\\red_correct.png")          #loads all of the photoes containning:
    bc = pygame.image.load(IMAGES_DIR + "main\\blue_correct.png")         #Yellow correct and incorrect ect.
    yc = pygame.image.load(IMAGES_DIR + "main\\orange_correct.png")
    gc = pygame.image.load(IMAGES_DIR + "main\\green_correct.png")
    inrc = pygame.image.load(IMAGES_DIR + "main\\red_incorrect.png")
    inbc = pygame.image.load(IMAGES_DIR + "main\\blue_incorrect.png")
    inyc = pygame.image.load(IMAGES_DIR + "main\\orange_incorrect.png")
    ingc = pygame.image.load(IMAGES_DIR + "main\\green_incorrect.png")
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
    questionFont = pygame.font.Font(get_font("BAUHS93"), 50)
    question_text = textbox.OutputBox(screen, question, (800, 70), (0, 30), (255, 255, 255), 0, (), (0, 0, 0), get_font("BAUHS93"))

    x = 20
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
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False

        screen.blit(basic_form, (0, 0))

        width = 395     #width of the rectengels
        height = 111    #height of the rectrngels
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
            pygame.display.flip()

            c = c + 0.1 if c + 0.1 <= 1 else 1

    return False


def exit_screen(screen, names, points):

    clock = pygame.time.Clock()

    sizes = [85, 85, 85]
    for i in range(3):
        answerFont = pygame.font.Font(None, sizes[i])
        while answerFont.size(names[i])[0] > 132:
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
        if current - last > 0.11:
            last = current
            screen.fill((87, 37, 194))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.fadeout(gif*100)
                    finish = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.fadeout(gif*100)
                    la_finito = True

            image = pygame.image.load(IMAGES_DIR + "win_background\\frame_%s_delay-0.04s.png" % str(gif % 178).zfill(3))
            screen.blit(image, (0, up))
            speed += 1

            if not la_finito:
                if current - start >= 7:
                    podioms[0] = podioms[0] - 6 if podioms[0] - 6 >= 0 else 0
                if current - start >= 14.5:
                    podioms[1] = podioms[1] - 6 if podioms[1] - 6 >= 0 else 0
                if current - start >= 23:
                    podioms[2] = podioms[2] - 6 if podioms[2] - 6 >= 0 else 0
            else:
                    podioms = [x + (178 - gif)/20 for x in podioms]


            answerFont = pygame.font.Font(None, sizes[0])
            answerText = answerFont.render(names[0], False, WHITE, TCHELET)
            textW, textH = answerFont.size(names[0])
            screen.blit(answerText, (WIDTH/2 - textW/2, final[0] + podioms[0] - textH))
            image = pygame.image.load(IMAGES_DIR + "winners_stand\\Slide1.png")
            image.set_colorkey(BLACK)
            screen.blit(image, (WIDTH/2 - 74, final[0] + podioms[0]))
            textbox.OutputBox(screen, str(points[0]) + " points!", (74*2, 45), (WIDTH/2 - 74, final[0] + podioms[0] + 90), None, 0, None, (255, 255, 255)).draw()

            answerFont = pygame.font.Font(None, sizes[1])
            answerText = answerFont.render(names[1], False, WHITE, TCHELET)
            textW, textH = answerFont.size(names[1])
            screen.blit(answerText, (WIDTH/2 - 74*3 - textW/2, final[1] + podioms[1] - textH))
            image = pygame.image.load(IMAGES_DIR + "winners_stand\\Slide2.png")
            image.set_colorkey(BLACK)
            screen.blit(image, (WIDTH/2 - 74*4, final[1] + podioms[1]))
            textbox.OutputBox(screen, str(points[1]) + " points!", (74*2, 45), (WIDTH/2 - 74*4, final[1] + podioms[1] + 90), None, 0, None, (255, 255, 255)).draw()

            answerFont = pygame.font.Font(None, sizes[2])
            answerText = answerFont.render(names[2], False, WHITE, TCHELET)
            textW, textH = answerFont.size(names[2])
            screen.blit(answerText, (WIDTH/2 + 74*3 - textW/2, final[2] + podioms[2] - textH))
            image = pygame.image.load(IMAGES_DIR + "winners_stand\\Slide3.png")
            image.set_colorkey(BLACK)
            screen.blit(image, (WIDTH/2 + 74*2, final[2] + podioms[2]))
            textbox.OutputBox(screen, str(points[2]) + " points!", (74*2, 45), (WIDTH/2 + 74*2, final[2] + podioms[2] + 90), None, 0, None, (255, 255, 255)).draw()

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
            largeText = pygame.font.Font(None, int(WIDTH/4/len(names[x])) - int(30/len(names[x])) + 5)
            name_text = largeText.render(names[x], False, BLACK)#print the name
            screen.blit(name_text, (x % 4 * (WIDTH / 4) + 20, 245 + int(x / 4) * 60))
        else:
            largeText = pygame.font.Font(None, 60)
            name_text = largeText.render(names[x], False, BLACK)  # prin
            screen.blit(name_text, (x % 4 * (WIDTH / 4), 230 + int(x / 4) * 60))

    pygame.display.flip()


def get_font(name):
    return FONT_LIB + name + ".ttf"


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