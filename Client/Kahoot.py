#-----------------------Imports-----------------------
import Client
import pygame


#-----------------------Globals-----------------------
username = None


#----------------------Functions----------------------
def login_screen():
    """
    Welcome, amigo!
    There is still a lot of work ahead of us, but I promise, it will be fun!

    TASK I:
        Program a login screen which gets a username as an input from the user and returns it.
        :return a username
    """
    global username
    username = raw_input("Choose username: ")  # <--- delete this
    return username


def username_taken():
    """
    Oooooooooops!
    Looks like you and another amigo were planing on using the same username and you weren't fast enough...  What a shameful lost!

    TASK II:
        Notify the user the username he had chosen is already used and he should chose a different one, Thou don't input it in this screen
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
    The server won't receive answers which were submitted late, and the client would crush!

    TASK III:
        Program the main screen.
        Screen must contain a way to input your answer - a number between 1, and 4
        'Client' also have a couple of functions which might be useful for decorating the "main_screen",
            - Client.time_left()
            - Client.get_place()
            - Client.get_score()
            - Client.get_behind()
        Go Crazzzzzzzzzzzzzzzzy!

        Bullet prof your screen so it won't continue running after time is up.

        :return The answer the user have choosen, 1 <= number <= 4
                OR None if he didn't have enough time
    """
    answer = raw_input("Your answer: ")  # <--- delete this
    if not Client.time_is_up():
        return int(answer)  # <---------------- write here
    return None


def results_screen(correct, wait_until):
    """
    Are you a secrete genius?
    Or the class's biggest foul?
    Well, amigo, today we find out!

    TASK IV:
        Program a "Horrrrray! Very Correct Answer Indeed." and a "Boooo! You Are A Loser!" screens
        :param correct: True for mastermind, False otherwise
        :return None
        *Stay inside this screen until the next question starts
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
    For example, When you login to our Kahoot but we are still waiting for other players to join. Or when you finish a question but there is still time left to answer it.

    TASK V:
        Program a loading screen so everyone would know they need to calm the fuck down once in a while.
        :param message: the reason for the delay
                        will be one of the following:
                            - "Waiting for the game to start..."
                            - "Waiting for question to end..."

        :param wait_until: what is blocking
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
        Make sure you let your client know what place he ended up getting by using "Client.get_place()".
        Do not close the program until the user says so!
        :return None
    """
    print "\nThe game is finished!\nYou won " + str(Client.get_place()) + " place with " + str(Client.get_score()) + " points!\nGood bye!\n"  # <---- delete this
    raw_input("\nPress 'Enter' to exit...")  # In my example, a simple "raw_input()" is used to wait until the user want to exit the program


#-------------------------Main-------------------------
def main():
    """
    Don't worry! We have got your back!
    All of the hard work was already done for you.
    Our server and your client already have a programmed protocol which you can access by our very helpful "Client" library.
    All that is left for you to do is to program your own unique User Interface, on which the client would run.
    How fun is that?!

    Everything is already sorted out in to functions. Each function is its own screen and should be programmed separately and independently,
    But do not open a new window for every function, that's just bad manners...

    That is all,
    GOOD LUCK, Amigo!
    """
    while not Client.login(login_screen()):  # loops as long as login was unsuccessful
        username_taken()
    loading("Waiting for the game to start...", lambda x: Client.question_in_progress())
    while not Client.end_game():  # loops as long as the questions are gonna keep coming
        if Client.question_in_progress():
            Client.send_answer(main_screen())
            loading("Waiting for question to end...", lambda x: not Client.question_in_progress())
        else:
            results_screen(Client.result(), lambda x: Client.question_in_progress())
    finish_screen()

if __name__ == '__main__':
    main()