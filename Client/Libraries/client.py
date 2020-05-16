#-----------------------Imports-----------------------
import os
import sys
sys.path.insert(0, os.getcwd()+'/files')
import ServerDitection
import traceback
import socket
from select import select
import time
import Libraries
sys.dont_write_bytecode = True


#-----------------------Globals-----------------------
IP = Libraries.IP
my_socket = Libraries.my_socket
username = None
game_finished = False
new_question = False
timer = None
answered_current = False

answer = None
score = None
behind = None
place = None
answers = None


#-----------------------Library-----------------------
def login(name):
    """
    Login to the our Kaboot server.
    :param name: your choosen username. len(name) <= 14
    :return: True -> Connected successfully
             False - > Username was taken
    """
    if '\r' in name or '\n' in name or '\t' in name:
        raise Exception("Usernames are not allowed to contain line breaks or tabs")
    if len(name) > 14:
        raise Exception("Name should be 14, characters or less!\nWe didn't give enough fuck to make our GUI more responsive.")
    try:
        global my_socket, username
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
        if not question_received():
            raise Exception("You are out of time")
        if answered_current:
            raise Exception("You have already answered the current question!")
        my_socket.send("answer: " + str(your_answer) + "\n")
        answered_current = True


def question_received():
    """
    :return True -> A question has started
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
    return timer - int(time.time()) < 0


def get_answers():
    """
    checks if the question has finished
    :return True -> if it did
            False -> if it didn't
    """
    global answers
    handle_server()
    if not timer:
        raise Exception("No question currently in progress")
    return answers


def result():
    """
    checks if your answer was correct or wrong
    :return True -> it was correct
            False -> it was wrong/no answer was received
    """
    global answer
    handle_server()
    if answer is None:
        raise Exception("Question is still in progress!")
    return answer


def get_score():
    """
    get your current score
    :return the amount of points you have collected so far
    """
    global my_socket, score
    my_socket.send('get_score\n')
    time.sleep(0.3)
    attemps = 1000000
    while not handle_server()['score']:
        attemps -= 1
        if attemps < 0:
            raise Exception("Server didn't respond.")
    return score


def get_behind():
    """
    antagonize yourself by knowing who is this cunt right in front of you
    :return HIM
            or None if you are in first place
    """
    global my_socket, score
    if get_place() > 1:
        my_socket.send('get_behind\n')
        time.sleep(0.3)
        attemps = 1000000
        while not handle_server()['behind']:
            attemps -= 1
            if attemps < 0:
                raise Exception("Server didn't respond.")
        return behind
    else:
        return None


def get_place():
    """
    tells you how well you did in compare to other student in your class
    :returns your place
    """
    global my_socket, score
    my_socket.send('get_place\n')
    time.sleep(0.3)
    attemps = 1000000
    while not handle_server()['place']:
        attemps -= 1
        if attemps < 0:
            raise Exception("Server didn't respond.")
    return place


def end_game():
    """
    Prepare your final_screen because this game is done, maybe...
    you can still preform 'get_place', 'get_score', or 'get_behind' functions after game is done.
    :return True -> game is finished
            False -> not yet
    """
    global game_finished
    handle_server()
    return game_finished


#----------------------Functions----------------------
#--------------------Back End Shit--------------------
#--------------------Do Not Touch!--------------------
def handle_server():
    """
    updates the server connection
    :return: a dictionary containing everything that was received. {result, score, behind, place}
    """
    global my_socket, game_finished, new_question, timer, behind, score, place, answer, answered_current, answers


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
            timer = int(time.time()) + int(data.split(": ")[1].split("[")[0]) - 1
            new_question = True
            answers = data.split("['")[1].split("']")[0].replace("\"", "\'").replace("\\n", "\n").split("', '")
            answer = None

        elif data[:len("score: ")] == "score: ":
            score = int(data.split(": ")[1])
            recieved['score'] = True

        elif data[:len("place: ")] == "place: ":
            place = int(data.split(": ")[1])
            recieved['place'] = True

        elif data[:len("behind: ")] == "behind: ":
            behind = data.split(": ")[1]
            recieved['behind'] = True

        elif data == "game_finished":
            game_finished = True

    return recieved

