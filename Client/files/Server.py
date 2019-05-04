#-----------------------Imports-----------------------
import socket
from select import select
import thread
import traceback
import os
import sys
sys.path.insert(0, os.getcwd()+'/files')
import ServerDitection


#-----------------------Globals-----------------------
__IP = "127.0.0.1"
# Gets local ip

__server_socket = socket.socket()
__server_socket.bind((__IP, 23))
__server_socket.listen(5)
# Creates server's socket

__mandatory = []
# Contains mandatory responses like login confirmations, get score command and such: [(socket1, 'OK'), (socket2, 'TAKEN'), ......]

open_client_sockets = []
# All connected sockets

__players = []
# A list of all players in the game


#-----------------------Classes-----------------------
class Player:
    def __init__(self, name, client_socket):
        self.name = name
        self.socket = client_socket
        self.score = 0
        self.answer = None

    def add_score(self, points):
        self.score += points

    def submit_answer(self, answer):
        self.answer = answer

    def delete_answer(self):
        self.answer = None


#----------------------Functions----------------------
def _error():
    print '\33[31m' + traceback.format_exc() + '\033[0m'


def __send__mandatory(wlist):
    """
    Sends waiting messages that are queued to be sent, but only if the client is writable
    :param wlist: a list of all the writable client sockets
    :return: None
    """
    global __mandatory
    for message in __mandatory:
        client_socket, data = message
        if client_socket in wlist:
            client_socket.send(data + '\n')
            __mandatory.remove(message)


def __handle_client_request(client_socket, request):
    """
    Appends a proper respond to the clients request
    :param client_socket: the user's socket
    :param request: what was received from the user
    :return: none
    """
    global __mandatory, open_client_sockets
    player = [x for x in __players if x.socket == client_socket]
    if player:
        player = player[0]
    if request[:len("login: ")] == "login: ":
        if request.split("login: ")[1] not in [x.name for x in __players]:
            __players.append(Player(request.split("login: ")[1], client_socket))
            __mandatory.append((client_socket, 'OK'))
        else:
            __mandatory.append((client_socket, 'TAKEN'))

    elif request[:len("answer: ")] == "answer: ":
        if player.answer is None:
            player.submit_answer(int(request.split("answer: ")[1]))

    elif request == "get_score":
        __mandatory.append((player.socket, "score: " + str(player.score)))

    elif request == "get_behind":
        __mandatory.append((player.socket, "behind: " + __players[__players.index(player)-1].name))

    elif request == "get_place":
        __mandatory.append((player.socket, "place: " + str(__players.index(player)+1)))
        

def __single_user(client_socket):
    """
    Messages a single client
    :param client_socket: the user's socket
    :return: none
    """
    global __server_socket
    if client_socket is __server_socket:
                new_socket, address = __server_socket.accept()
                open_client_sockets.append(new_socket)
                print "Connected with client."
    else:
        try:
            data = ''
            while '\n' not in data:
                data += client_socket.recv(1)
            data = data.replace('\n', '')
            if data:
                __handle_client_request(client_socket, data)
            else:
                open_client_sockets.remove(client_socket)
                print "Connection with client closed."
        except socket.error:
            open_client_sockets.remove(client_socket)


#-----------------------Library-----------------------
def update_login():
    """
    Manages all the server's clients login attempts.
    automatically sends a respond to the client
    :return: a list of all logged in users
    """
    global __server_socket
    rlist, wlist, xlist = select([__server_socket] + open_client_sockets, open_client_sockets, open_client_sockets, 0.1)
    for current_socket in rlist:
        __single_user(current_socket)
    for current_socket in xlist:
        open_client_sockets.remove(current_socket)
    __send__mandatory(wlist)
    return [x.name for x in __players]


def receive():
    """
    receives all of the players answers and saves them but doesn't respond yet in addition to answering trier mandatory requests.
    :return: none
    """
    global __server_socket
    rlist, wlist, xlist = select([__server_socket] + open_client_sockets, open_client_sockets, open_client_sockets, 0.1)
    for current_socket in rlist:
        __single_user(current_socket)
    for current_socket in xlist:
        open_client_sockets.remove(current_socket)
    __send__mandatory(wlist)


def results(correct_answer, score):
    """
    Sends all players a respond which indicates if their answer was correct or wrong
    :param correct_answer: the number of the correct answer
    :param score: the amount of points each player will gain if he answered correctly
    :return: a dictionary containing all players and their corresponding score, sorted from highest to lowest
    """
    global __server_socket
    rlist, wlist, xlist = select([__server_socket] + open_client_sockets, open_client_sockets, open_client_sockets, 0.1)
    for player in __players:
        client_socket, answer = player.socket, player.answer
        if answer == correct_answer:
            respond = 'True'
            player.add_score(score)
        else:
            respond = 'False'
        if client_socket in wlist:
            client_socket.send(respond + '\n')

    for current_socket in xlist:
        open_client_sockets.remove(current_socket)
    #flush all answers
    for player in __players:
        player.answer = None
    __players.sort(key=lambda x: x.score, reverse=True)
    return {x.name: x.score for x in __players}


def new_question(time):
    """
    Notifies all players that there is a new question available for them to answer
    :param time: how much time they have to answer the question
    :return: None
    """
    for player in __players:
        __mandatory.append((player.socket, 'new: ' + str(time)))
    rlist, wlist, xlist = select([__server_socket] + open_client_sockets, open_client_sockets, open_client_sockets, 0.1)
    __send__mandatory(wlist)


def get_players():
    """
    Returns a dictionary containing all players and their corresponding score, sorted from highest to lowest
    """
    return {x.name: x.score for x in __players}


def end_game():
    """
    notifies all players that the game has ended
    """
    for player in __players:
        __mandatory.append((player.socket, 'game_finished'))
    rlist, wlist, xlist = select([__server_socket] + open_client_sockets, open_client_sockets, open_client_sockets, 0.1)
    __send__mandatory(wlist)