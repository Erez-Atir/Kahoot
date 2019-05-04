#-----------------------Imports-----------------------
import os
import sys
sys.path.insert(0, os.getcwd()+'/files')
import ServerDitection
import traceback
import socket
from select import select
import time


#-----------------------Globals-----------------------
IP = None
my_socket = None
username = None
game_finished = False
new_question = False
timer = None
answered_current = False

answer = None
score = None
behind = None
place = None


#----------------------Functions----------------------
def error():
    print '\33[31m' + traceback.format_exc() + '\033[0m'


def handle_server():
    """
    updates the server connection
    :return: a dictionary containing everything that was received. {result, score, behind, place}
    """
    global my_socket, game_finished, new_question, timer, behind, score, place, answer, answered_current


    rlist, wlist, xlist = select([my_socket], [my_socket], [my_socket], 0.1)
    recieved = {'result': False, 'score': False, 'behind': False, 'place': False}
    if rlist:
        data = ''
        while '\n' not in data:
            data += rlist[0].recv(1)
        data = data.replace('\n', '')
        if data == "True":
            answer = True
            recieved['result'] = True
            new_question = False
            timer = None
            answered_current = False
        elif data == "False":
            answer = False
            recieved['result'] = True
            new_question = False
            timer = None
            answered_current = False

        elif data[:len("new: ")] == "new: ":
            timer = int(time.time()) + int(data.split(": ")[1])
            new_question = True
            answer = None

        elif data[:len("score: ")] == "score: ":
            score = data.split(": ")[1]
            recieved['score'] = True

        elif data[:len("place: ")] == "place: ":
            place = data.split(": ")[1]
            recieved['place'] = True

        elif data[:len("behind: ")] == "behind: ":
            behind = data.split(": ")[1]
            recieved['behind'] = True

        elif data == "game_finished":
            game_finished = True

    return recieved


#-----------------------Library-----------------------
def _real_run():
    """
    This is a very very secretive function.
    You don't need to use it until we tell you...
    """
    global IP, my_socket
    IP = ServerDitection.server_scout().split("Here Be Server: ")[1]
    my_socket = socket.socket()
    my_socket.connect((IP, 23))


def login(name):
    """
    Logins to the our Kahoot server.
    :param name: your choosen name
    :return: True -> Connected succefully
             False - > Username was taken
    """
    if '\r' in name or '\n' in name or '\t' in name:
        raise Exception("Usernames are not allowed to contain line breaks or tabs")
    try:
        global my_socket, username, IP
        if not my_socket:
            IP = "127.0.0.1"
            my_socket = socket.socket()
            my_socket.connect((IP, 23))

        my_socket.send("login: " + name + "\n")
        data = ''
        while '\n' not in data:
            data += my_socket.recv(1)
        if data == "OK\n":
            username = name
            return True
        else:
            return False
    except Exception:
        raise Exception("Login failed!\nPlease make sure the \"test_server\" is up")


def question_in_progress():
    """
    :return True -> A new question has received
            False -> New question didn't start yet
    """
    global new_question
    handle_server()
    return new_question


def time_left():
    """
    :return How much seconds are left for the current question
    """
    global timer
    handle_server()
    if not timer:
        raise Exception("No question currently in progress")
    return timer - int(time.time())


def time_is_up():
    """
    checks if the question has finished
    :return True -> if it did
            False -> if it didn't
    """
    global timer
    handle_server()
    if not timer:
        return True
    return timer - int(time.time()) <= 0


def result():
    """
    checks if your answer was correct of wrong
    :return True -> it was correct
            False -> it was wrong or no answer was received
    """
    global answer
    handle_server()
    if answer is None:
        raise Exception("Question is still in progress!")
    return answer


def get_score():
    """
    get your current score
    :return your points
    """
    global my_socket, score
    my_socket.send('get_score\n')
    time.sleep(0.3)
    attemps = 10000
    while not handle_server()['score']:
        attemps -= 1
        if attemps < 0:
            raise Exception("Server didn't respond.")
    return score


def get_behind():
    """
    antagonize yourself by knowing who is this cunt right in front of you
    :return HIM
    """
    global my_socket, score
    my_socket.send('get_behind\n')
    time.sleep(0.3)
    attemps = 10000
    while not handle_server()['behind']:
        attemps -= 1
        if attemps < 0:
            raise Exception("Server didn't respond.")
    return behind


def get_place():
    """
    tells you how well you did in compare to the other class
    :returns the amount of points you have collected so far
    """
    global my_socket, score
    my_socket.send('get_place\n')
    time.sleep(0.3)
    attemps = 10000
    while not handle_server()['place']:
        attemps -= 1
        if attemps < 0:
            raise Exception("Server didn't respond.")
    return place


def end_game():
    """
    Prepare you final results screen because this game is done
    you can still preform get_place, get_score, or get_behind after game is done.
    :return True -> game is finished
            False -> not yet
    """
    global game_finished
    handle_server()
    return game_finished


def send_answer(your_answer=None):
    """
    Sends your answer to the current question to the server.
    :return None
    """
    if your_answer:
        if your_answer < 1 or your_answer > 4:
            raise Exception("Answer can only be a number between 1 and 4!\nYou've chosen " + str(your_answer) + "!")
        global my_socket, answered_current
        handle_server()
        if not question_in_progress():
            raise Exception("You are out of time")
        if answered_current:
            raise Exception("You have already answered the current question!")
        my_socket.send("answer: " + str(your_answer) + "\n")
        answered_current = True



