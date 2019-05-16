#-----------------------Imports-----------------------
from Client.Libraries import client


#-----------------------Globals-----------------------
username = None


#-------------------------Main-------------------------
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
    while not client.login(login_screen()):
        username_taken()
    loading("Waiting for the game to start...", lambda x: client.question_received())
    while not client.end_game():
        if client.question_received():
            client.send_answer(main_screen())
            if client.question_received():
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
    global username
    username = raw_input("Choose username: ")  # <--- delete this
    return username


def username_taken():
    """
    Ooooooooooooooooooooooooops!
    Looks like you and another amigo were planing on using the same username and you weren't fast enough...  What a shameful lost!

    TASK II:
        Notify the user the username he had chosen is already used and he should chose a different one, Thou don't input it at this screen
        :return None
    """
    print "Username is taken!"  # <--- delete this


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
    answer = int(raw_input("Your answer: "))  # <--- delete this
    while not client.time_is_up():
        return answer  # <---------------- write here
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
    if correct:
        print "Your answer was correct"  # <--- delete this
        while not wait_until(''):
            pass  # <-------------------------- wright here
    else:
        print "Your answer was wrong"  # <--- delete this
        while not wait_until(''):
            pass  # <------------------------ wright here


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
    print message  # <--------------- delete this
    while not wait_until(''):
        pass  # <-------------------- wright here


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
    print "\nThe game is finished!\nYou won " + str(client.get_place()) + " place with " + str(client.get_score()) + " points!\nGood bye!\n"  # <---- delete this
    raw_input("\nPress 'Enter' to exit...")  # In my example, a simple "raw_input()" is used to wait until the user wants to exit the program


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
