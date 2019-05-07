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
if not os.path.exists(IMAGES_DIR):#if path doesn't exists
    IMAGES_DIR = os.getcwd()      #set the default to the libary from which the code runs

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
    if os.path.exists(IMAGES_DIR + "log_screen.png"): #if path to an image exists
        log_screen = pygame.image.load(IMAGES_DIR + "log_screen.png")#load image
        screen.blit(log_screen, (0,0))
        pygame.display.flip()
    else:                                             #else
        log_screen = pygame.Surface((WIDTH, HEIGHT))  #load nothing
    if os.path.exists(IMAGES_DIR + "log_screen_start_selected.png"): #if path to an image exists
        log_screen_start_selcted = pygame.image.load(IMAGES_DIR + "log_screen_start_selected.png") #load image
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
                """if 25 < x and x < 770 and y > 490 and y <580:#if mouse above start button
                    screen.blit(log_screen_start_selcted, (0,0))#fill the screen with bold "start" image
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)#set cursor to broken x"""

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
        exit = add_question(screen, 5, "The correct answer is number 3", ["1", "2", "3", "4"], 1, None, 15, 1000)
    #if not exit:
    #        exit = add_question(screen, 5, "Who shot the sheriff?", ["I shot the sheriff", "but I did not shoot the deputy", "It was santa!", "Chuck Norris did it!"], 3, None, 10, 800)
    #if not exit:
    #    exit = add_question(screen, 5, "Is this the real life?", ["It's just a fantasy.", "Caught in a landslide", "No escape from reality", "Open your eyes"], 4, None, 10, 800)
    if not exit:
        Server.end_game()
        for buffer in xrange(100):
            Server.receive()
        players = Server.get_players().keys()
        exit_screen(screen, players[0], players[1], players[2])
    pygame.quit()



def exit_screen(screen, name1, name2, name3):
    pygame.mixer.music.load(OST_DIR + "winners.mp3")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()


    gif = 0
    speed = 1
    sub = False
    finish = False
    la_finito = False
    up = 0
    final_place = [170, 215, 303]
    down = [220, 280, 360]
    last = time.time()
    while not finish:
        Server.receive()
        current = time.time()
        if current - last > 0.1:
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
                if gif > 50:
                    down = [x-10 if x-6 >= 0 else x for x in down]
                elif gif > 60:
                    down = [x-4 if x-3 >= 0 else x for x in down]
                elif gif > 70:
                    down = [x-2 if x-2 >= 0 else x for x in down]
                elif gif > 50:
                    down = [x-1 if x-1 >= 0 else x for x in down]
            else:
                if gif < 50:
                    down = [x+12 for x in down]
                elif gif < 60:
                    down = [x+10 for x in down]
                elif gif < 70:
                    down = [x+8 for x in down]
                elif gif < 85:
                    down = [x+6 for x in down]
                elif gif < 110:
                    down = [x+4 for x in down]


            answerFont = pygame.font.Font(get_font("bauhaus93"), int(60 - (len(name1)*4)))
            answerText = answerFont.render(name1, False, WHITE)
            screen.blit(answerText, (460, final_place[0] - down[0]))
            answerText = answerFont.render(name2, False, WHITE)
            screen.blit(answerText, (243, final_place[1] - down[1]))
            answerText = answerFont.render(name3, False, WHITE)
            screen.blit(answerText, (350, final_place[2] - down[2]))
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
            exit = load_question(screen, question, photo, answers, correct_answer ,qtime, points) #"""calls a function to print the question"""
            if not exit:
                pass
            else:
                return True
        else:
            return True
        return False


def load_question(screen, question, photo, answers, correct_answer, qtime, qpoints):
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
        image = pygame.image.load(IMAGES_DIR + "questions.png")
    else:
        image = pygame.image.load(IMAGES_DIR + "questions_no_image.png")

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
    PLAYERSSCORE = Server.results(correct_answer, qpoints)
    pygame.mixer.music.fadeout(2000)
    return False


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


def load_timer(num, screen, question):
    first = time.time()
    last = time.time()
    angle = 19
    #already_rotated = 0
    questionFont = pygame.font.Font(get_font("bauhaus93"), 50)
    questionText = questionFont.render(question, False, BLACK)
    current = time.time()
    count = 0
    while current - first <= num + 1:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                return True
        current = time.time()
        if current - last > 0.05:
            hamster_img = pygame.image.load(IMAGES_DIR + "hamster_pos" +  str(count % 4 + 1) + ".png")
            hamster_img.set_colorkey((255, 255, 255))
            #already_rotated = (already_rotated + 3) % 360
            #loading_image = pygame.transform.rotate(image, already_rotated)

            image = pygame.image.load(IMAGES_DIR + "loading\\frame_%s_delay-0.04s.png" % str(angle).zfill(2))
            image.set_colorkey((0, 0, 0))
            screen.blit(BLACKSURFACE, (0, 0))
            #print(len(str(int(num - current + first + 1))))
            x = 20 # width of a letter, change according to the font
            screen.blit(questionText, (int((WIDTH/x - len(question))/2 * x), 312))
            screen.blit(hamster_img, (324, 30))
            screen.blit(image, (300, 95))
            timerFont = pygame.font.Font(get_font("bauhaus93"), 150)
            timerText = timerFont.render(str(num - int(current - first)), False, BLACK)
            if len(str(int(num - current + first + 1))) == 2:
                screen.blit(timerText, (340, 155))
            else:
                screen.blit(timerText, (370, 155))
            pygame.display.flip()
            last = current
            count += 1
            if angle > 0:
                angle -= 1
            else:
                angle = 19
    return False


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