#-----------------------Imports-----------------------
import pygame
from Libraries import textbox, client
import os
import time


#-----------------------Globals-----------------------
username = None
RED = (204, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 153, 0)
BLUE = (53, 119, 252)
PURPLE = (176, 71, 246)
GREY = (85, 77, 77)
ORANGE = (255, 181, 30)
screen = pygame.display.set_mode((600, 400))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
clock = pygame.time.Clock()
REFRESH_RATE = 32
IMAGES_DIR = os.getcwd() + "\\images\\" #saves the path to the images libary
img = [pygame.image.load(IMAGES_DIR + "loading_cat\\frame_%s_delay-0.03s.png" % str(x).zfill(2)) for x in xrange(90)]
size = img[0].get_rect().size
if pygame.transform.scale(img[0], (int(size[0]/600.*HEIGHT), int(size[1]/600.*HEIGHT))).get_rect().size[0] <= WIDTH:
    for image in range(len(img)):
        size = img[image].get_rect().size
        img[image] = pygame.transform.scale(img[image], (int(size[0]/600.*HEIGHT), int(size[1]/600.*HEIGHT)))
else:
    for image in range(len(img)):
        size = img[image].get_rect().size
        img[image] = pygame.transform.scale(img[image], (int(size[0]/800.*WIDTH), int(size[1]/800.*WIDTH)))
size = img[0].get_rect().size
#-------------------------Main-------------------------


def resfix(x=None, y=None):
    """
    because we didn't instruct the class on how to make your program responsive
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
            sizee = x.get_rect().sizee
            return pygame.transform.scale(x, (int(sizee[0]/800.*WIDTH), int(sizee[1]/600.*HEIGHT)))
    if y is not None:
        return int(y/800.*HEIGHT)
    return None


def main():
    """
    Don't worry! We have got your back!
    All of the hard work was already done for you.
    Our server and your client already have a programmed protocol which you can access by our very helpful "client" library.
    All that is left for you to do is to program your own unique User Interface, on which the client would run.
    How fun is that?!

    Everything is already sorted out in to functions. Each function is its own screen and should be programmed separately and independently,
    But do not open a new window for every function, that's just bad manners...

    To your assist, we have programmed two libraries:
        - client
        - textbox
        To see a library's abilities enter its file and read its fucking manual, below the #---Library--- stamp

    That is all,
    GOOD LUCK, Amigo!
    """
    global screen
    while not client.login(login_screen()):
        username_taken()
    loading("Waiting for the game to start...", lambda x: client.question_received())
    while not client.end_game():
        if client.question_received():
            answer = main_screen()
            client.send_answer(answer)
            if answer and client.question_received():
                loading("Waiting for question to end...", lambda x: not client.question_received())
        else:
            results_screen(client.result(), lambda x: client.question_received() or client.end_game())
    finish_screen()


#----------------------Functions----------------------
def login_screen():
    """
    Welcome, amigo!
    There is still a lot of work ahead of us, but I promise, it will be fun!

    TASK I:
        Program a login screen which gets a username as an input from the user and returns it.
        You can use the textbox library which we programmed just for you in order to create an "InputBox"
        :return a username
    """
    global username, screen
    screen.fill(PURPLE)
    a = textbox.OutputBox(screen=screen, text="KABOOT!", size=resfix(1000, 200), place=resfix(250, 50), color=PURPLE,
                      border_width=0, border_color=PURPLE, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")
    b = textbox.OutputBox(screen=screen, text="Enter your username:", size=resfix(500, 100), place=resfix(500, 250), color=PURPLE,
                      border_width=0, border_color=PURPLE, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")
    login = textbox.InputBox(screen=screen, size=resfix(750, 80), place=resfix((1500-750)/2, 360), color=(255, 255, 255), border_width=2, border_color=BLACK, limit=12, font="files\\montserrat\\Montserrat-Black.otf")
    button = textbox.OutputBox(screen=screen, text="Enter", size=resfix(320, 80), place=resfix(590, 480), color=GREY,
                          border_width=0, border_color=PURPLE, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")

    finish = False
    while not finish:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == 2 and event.key == 13:
                finish = True if username else False
            if event.type == pygame.QUIT:#user presses the X
                exit()
            if event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    exit()
        if resfix(590+320) > mouse[0] > resfix(590) and resfix(None, 480+80) > mouse[1] > resfix(None, 480) and pygame.mouse.get_pressed()[0]:
            finish = True if username else False
        a.draw()
        b.draw()
        login.draw()
        button.draw()
        pygame.display.flip()
        username = login.get_input()
    return username


def username_taken():
    """
    Ooooooooooooooooooooooooops!
    Looks like you and another amigo were planing on using the same username and you weren't fast enough...  What a shameful lost!

    TASK II:
        Notify the user the username he had chosen is already used and he should chose a different one, Thou don't input it at this screen
        :return None
    """
    global username, screen
    screen.fill(PURPLE)
    a = textbox.OutputBox(screen=screen, text="KABOOT!", size=resfix(1000, 200), place=resfix(250, 50), color=PURPLE,
                      border_width=0, border_color=PURPLE, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")
    b = textbox.OutputBox(screen=screen, text="Username taken!\nPress 'Enter' to continue...", size=resfix(700, 200), place=resfix(400, 315), color=PURPLE,
                      border_width=0, border_color=PURPLE, text_color=RED, font="files\\montserrat\\Montserrat-Black.otf")

    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == 2 and event.key == 13:
                finish = True
            if event.type == pygame.QUIT:#user presses the X
                exit()
            if event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    exit()
        a.draw()
        b.draw()
        pygame.display.flip()


def main_screen():
    """
    That was fun! wasn't it?
    Now, let's really get to business!

    This is the screen where the user can choose an answer while a question is up.
    BE CAREFUL!
    If the user doesn't have enough time to answer the question the function must return None.
    The server won't accept answers which were submitted late, and the client would crush!

    TASK III:
        Program the main screen.
        Screen must contain a way to input your answer - a number between 1, and 4
        Do not wait for the "time_is_up" if an answer is chosen before hands, return it at the moment
        The "client" library has a bunch of function you can use to decorate the screen

        :return The answer the user had choosen, 1 <= number <= 4
                OR None if he didn't have enough time
    """
    global screen
    answers = client.get_answers()
    button1 = textbox.OutputBox(screen=screen, text=answers[0], size=resfix(735, 385), place=resfix(10, 10), color=RED,
                                border_width=0, border_color=WHITE, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")
    button2 = textbox.OutputBox(screen=screen, text=answers[1], size=resfix(735, 385), place=resfix(755, 10), color=BLUE,
                                border_width=0, border_color=WHITE, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")
    button3 = textbox.OutputBox(screen=screen, text=answers[2], size=resfix(735, 385), place=resfix(10, 405), color=ORANGE,
                                border_width=0, border_color=WHITE, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")
    button4 = textbox.OutputBox(screen=screen, text=answers[3], size=resfix(735, 385), place=resfix(755, 405), color=GREEN,
                                border_width=0, border_color=WHITE, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")
    timer = textbox.OutputBox(screen=screen, text="", size=(size[0]/3, size[1]/3), place=((WIDTH-size[0])/2+size[0]/3, (HEIGHT-size[1])/2+size[1]/3), color=None, border_width=0, border_color=BLACK, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")

    while not client.time_is_up():
        mouse = pygame.mouse.get_pos()
        x, y = mouse
        for event in pygame.event.get():
            if event.type == 2 and event.key == 13:
                finish = True
            if event.type == pygame.QUIT:#user presses the X
                exit()
            if event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    exit()
        if pygame.mouse.get_pressed()[0]:
            if resfix(10) < x < resfix(10+735) and resfix(None, 10) < y < resfix(None, 10+385):
                return 1
            if resfix(755) < x < resfix(755+735) and resfix(None, 10) < y < resfix(None, 10+385):
                return 2
            if resfix(10) < x < resfix(10+735) and resfix(None, 405) < y < resfix(None, 405+385):
                return 3
            if resfix(755) < x < resfix(755+735) and resfix(None, 405) < y < resfix(None, 405+385):
                return 4

        thymin = client.time_left()
        timer.text = str(thymin) if thymin >= 0 else str(0)
        pygame.draw.circle(screen, PURPLE, resfix(1500/2, 800/2), resfix(100))
        timer.draw()

        screen.fill(WHITE)
        button1.draw()
        button2.draw()
        button3.draw()
        button4.draw()
        #pygame.draw.polygon(screen, WHITE, [resfix(735/2, 61), resfix(194, 350), resfix(546, 350)])
        #pygame.draw.polygon(screen, WHITE, [resfix(1144, 61), resfix(755+230, 61+(350-61)/2), resfix(1144, 350), resfix(2*1144-(755+210)-20, 61+(350-61)/2)])
        #pygame.draw.polygon(screen, WHITE, [resfix(755+230, 405+61), resfix(755+230, 405+350), resfix(2*1144-(755+210)-20, 405+350), resfix(2*1144-(755+210)-20, 405+61)])
        #pygame.draw.circle(screen, WHITE, resfix(735/2, 405+385/2+15), resfix((350-61)/2+5))

        pygame.display.flip()

    pygame.draw.circle(screen, PURPLE, resfix(1500/2, 800/2), resfix(100))
    pygame.display.flip()
    return None


def results_screen(correct, wait_until):
    """
    Are you a secrete genius?
    Or the class's biggest foul?
    Well, amigo, today we find out!

    :param correct: True for mastermind, False otherwise
    :param wait_until: exit condition. don't touch!

    TASK IV:
        Program a "Horrrrray! Very Correct Answer Indeed." and a "Boooooo! You Are A Loser!" screens
        The "client" library has a bunch of function you can use to decorate the screen
        :return None
    """
    global screen
    name = textbox.OutputBox(screen=screen, text=username, size=resfix(200, 50), place=resfix(1500-204, 800-54), color=WHITE, border_width=2, border_color=BLACK, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf")

    place = client.get_place()
    if place == 1:
        text = "YOU ARE IN FIRST PLACE! YOU HAVE " + str(client.get_score()) + " POINTS!"
    elif place == 2:
        text = "You are in SECOND place with " + str(client.get_score()) + " points!"
    elif place == 3:
        text = "You are in THIRD place with " + str(client.get_score()) + " points!"
    else:
        text = "You are in " + str(place) + "TH place with " + str(client.get_score()) + " points!"
    stats = textbox.OutputBox(screen=screen, text=text, size=resfix(1000, 200), place=resfix(250, 500),
                      color=None, border_width=0, border_color=None, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")
    if correct:
        msg = textbox.OutputBox(screen=screen, text="Horrrrray!\nVery Correct Answer Indeed", size=resfix(1000, 400),
                          place=resfix(250, 100), color=GREEN, border_width=0, border_color=GREEN, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")

        while not wait_until(''):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:#user presses the X
                    exit()
                if event.type == pygame.KEYDOWN:
                    # If pressed key is ESC quit program
                    if event.key == pygame.K_ESCAPE:
                        exit()
            screen.fill(GREEN)
            msg.draw()
            name.draw()
            stats.draw()
            pygame.display.flip()
    else:
        msg = textbox.OutputBox(screen=screen, text="Boooooo!\nYou Are A Loser!", size=resfix(1000, 400), place=resfix(250, 100),
                          color=RED, border_width=0, border_color=RED, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")
        while not wait_until(''):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:#user presses the X
                    exit()
                if event.type == pygame.KEYDOWN:
                    # If pressed key is ESC quit program
                    if event.key == pygame.K_ESCAPE:
                        exit()
            screen.fill(RED)
            msg.draw()
            name.draw()
            stats.draw()
            pygame.display.flip()



def loading(message, wait_until):
    """
    HOLD UP! Why are you in a rush! Chill, amigo. Somethings in life take time, you know.
    Like what, you ask?!
    For example, When you login to our Kaboot but we are still waiting for other players to join in.
    Or when you finish a question but there is still time left to answer it.

    :param message: the reason for the delay
                will be one of the following:
                    - "Waiting for the game to start..."
                    - "Waiting for question to end..."

    :param wait_until: exit condition. don't touch!

    TASK V:
        Program a loading screen so everyone would know they need to calm the fuck down once in a while.
        :return nothing
    """
    global screen, img, size
    name = textbox.OutputBox(screen=screen, text=username, size=resfix(200, 50), place=resfix(1500-204, 800-54), color=WHITE, border_width=2, border_color=BLACK, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf")
    msg = textbox.OutputBox(screen=screen, text=message, size=resfix(1200, 150), place=resfix(150, 15), color=PURPLE, border_width=0, border_color=BLACK, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")
    timer = textbox.OutputBox(screen=screen, text="", size=(size[0]/3, size[1]/3), place=((WIDTH-size[0])/2+size[0]/3, (HEIGHT-size[1])/2+size[1]/3), color=None, border_width=0, border_color=BLACK, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")

    gif = 35
    while not wait_until(''):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:#user presses the X
                    exit()
                if event.type == pygame.KEYDOWN:
                    # If pressed key is ESC quit program
                    if event.key == pygame.K_ESCAPE:
                        exit()

        if message == "Waiting for question to end...":
            thymin = client.time_left()
            timer.text = str(thymin) if thymin >= 0 else str(0)
        screen.fill(PURPLE)
        msg.draw()
        screen.blit(img[gif], ((WIDTH-size[0])/2, (HEIGHT-size[1])/2))
        clock.tick(REFRESH_RATE)
        gif += 1
        if gif == 90:
            gif = 0
        name.draw()
        timer.draw()
        pygame.display.flip()
    screen.fill(PURPLE)
    msg.draw()
    name.draw()
    pygame.display.flip()




def finish_screen():
    """
    Well, it's been a pleasure working with you,
    but everything eventually must come to an end.
    Before our farewells, there is still one last thing.

    TASK VI:
        Make an ending screen indicating that the game is over.
        Make sure you let your client know what place he ended up getting.
        Do not close the program until the user says so!
        :return None
    """
    global screen
    place = client.get_place()
    name = textbox.OutputBox(screen=screen, text=username, size=resfix(200, 50), place=resfix(1500-204, 800-54), color=WHITE, border_width=2, border_color=BLACK, text_color=BLACK, font="files\\montserrat\\Montserrat-Black.otf")
    if place == 1:
        text = "YOU WON FIRST PLACE! YOU HAVE " + str(client.get_score()) + " POINTS!\nWell Done!\n"
    elif place == 2:
        text = "You finished in SECOND place with " + str(client.get_score()) + " points!\nGood job!\n"
    elif place == 3:
        text = "You finished in THIRD place with " + str(client.get_score()) + " points!\nGood bye!\n"
    else:
        text = "You finished in " + str(place) + "TH place with " + str(client.get_score()) + " points!\nGood bye!\n"
    finish = False
    if place == 1:
            box = textbox.OutputBox(screen=screen, text="You Won!", size=resfix(1300, 500), place=resfix(100, 00),
                              color=PURPLE, border_width=0, border_color=PURPLE, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")
    else:
        box = textbox.OutputBox(screen=screen, text="The game is finished!", size=resfix(1300, 500), place=resfix(100, 00),
                          color=PURPLE, border_width=0, border_color=PURPLE, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")

    stats = textbox.OutputBox(screen=screen, text=text, size=resfix(1000, 200), place=resfix(250, 500),
                      color=None, border_width=0, border_color=None, text_color=WHITE, font="files\\montserrat\\Montserrat-Black.otf")
    while not finish:
        for event in pygame.event.get():
            if event.type == 2 and event.key == 13:
                finish = True
            if event.type == pygame.QUIT:#user presses the X
                    exit()
            if event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    exit()
        screen.fill(PURPLE)
        box.draw()
        stats.draw()
        name.draw()
        pygame.display.flip()


def gui_is_ready():
    """
    That's it, amigo!
    Farewell!

    Task VII:
        Contact one of the project managers and tell them you have finished you GUI.
        We want to appreciate how well made it is, and also to instruct you how to connect to the real Kaboot.
    """
    pass


if __name__ == '__main__':
    gui_is_ready()
    main()