USER FUNCTIONS
import connectfour

def start_game()->connectfour.GameState:
    '''
    creates new game and displays a blank board
    '''
    game = connectfour.new_game()
    display_board(game)
    return game



def catch_drop(game: connectfour.GameState, col: int)->connectfour.GameState:
    '''
    Drops a piece in a given column and returns any possible errors
    '''
    try:
        game = connectfour.drop(game, col)
    except ValueError:
        print('ERROR: Invalid Column')
    except connectfour.InvalidMoveError:
        print('ERROR: Invalid Move')
    except connectfour.GameOverError:
        print('Game Over')
    finally:
        return game


def catch_pop(game:connectfour.GameState, col: int) -> connectfour.GameState:
    '''
    pops a piece from a given column and returns any possible errors
    '''
    try:
        game = connectfour.pop(game, col)
    except ValueError:
        print('ERROR: Invalid Column')
    except connectfour.InvalidMoveError:
        print('ERROR: Invalid Move')
    except connectfour.GameOverError:
        print('Game Over')
    finally:
        return game

def int_input()->int:
    '''
    Asks for a valid input for a column
    '''
    result = int()                               #
    try:
        result = int(input('Select a column (1-7): '))
    except (TypeError, ValueError):
        print('ERROR: Invalid Input')
        return int_input()
    else:
        return result - 1 #connect four library functions are 0-indexed

def display_board(game: connectfour.GameState):

    '''Displays current board when called'''
    col_array = game.board
    for n in range(1, connectfour.BOARD_COLUMNS+1): #display col #s
        print(n, end=' ')
    print()
    for i in range(0, connectfour.BOARD_ROWS): #displays board
        for col in col_array:
            if col[i] == 0:
                print('.', end=' ')
            elif col[i] == 1:
                print('R', end=' ')
            elif col[i] == 2:
                print('Y', end=' ')
        print()

def get_move()->int:
    '''
    Asks user for choice of move
    '''
    move = input('Pop or Drop? (P/D)').upper()
    if move == 'P':
        return 0
    elif move == 'D':
        return 1
    else:
        print('ERROR: Invalid Input')
        return get_move()

def check_winner(game: connectfour.GameState)->bool:
    '''
    Checks for a winner in the current gamestate by trying to drop in a column
    '''
    try:
        for i in range(0,7):
            try:
                connectfour.drop(game, i)
            except connectfour.InvalidMoveError:
                pass
        return False
    except connectfour.GameOverError:
        winner = connectfour.winner(game)
        print('Game Over')
        if winner == 1:
            print('Red Wins')
        elif winner == 2:
            print('Yellow Wins')
        return True







CONSOLE UI

import connectfour
import userfunctions


def console_drop(game: connectfour.GameState) -> connectfour.GameState:
    '''
    Drops a piece in the console only game mode
    '''
    col = userfunctions.int_input()
    game = userfunctions.catch_drop(game, col)
    userfunctions.display_board(game)
    return game
def console_pop(game: connectfour.GameState) -> connectfour.GameState:
    '''
    Pops a piece in the console only game mode
    '''
    col = userfunctions.int_input()
    game = userfunctions.catch_pop(game, col)
    userfunctions.display_board(game)
    return game

def main():
    game = userfunctions.start_game()
    while userfunctions.check_winner(game) is False:
        move = userfunctions.get_move()
        if move == 0:
            game = console_pop(game)
        elif move == 1:
            game = console_drop(game)




if __name__ == '__main__':
    main()






ONLINE UI

import connectfour
import userfunctions
import online

def user_move(game: connectfour.GameState, client: online.Client)-> connectfour.GameState:
    '''
    makes a move in the client-side game board and sends the move to the server
    '''
    move = userfunctions.get_move()
    col = userfunctions.int_input()
    if move == 0:
        game = userfunctions.catch_pop(game, col)
    elif move == 1:
        game = userfunctions.catch_drop(game, col)
    userfunctions.display_board(game)
    online.send_move(client, col + 1, move)#add 1 because int_input subtracts 1
    return game

def server_move(game: connectfour.GameState, client: online.Client)-> connectfour.GameState:
    '''
    Accepts a move from the server and updates it in the client side game board
    '''
    move = online.parse_msg(client)
    if move[1] >= 0:
        if move[0] < 10:
            col = move[0]
            game = userfunctions.catch_pop(game, col)
            userfunctions.display_board(game)
            return game
        elif move[0] >= 10:
            col = move[0] - 10
            game = userfunctions.catch_drop(game, col)
            userfunctions.display_board(game)
            return game
        elif move[0] == -1:
            userfunctions.display_board(game)
            return game


def main():
    client = online.input_host()
    if client == None:
        print('FATAL ERROR: Failed to connect')
        return
    try:
        online.ics_connect(client)
    except ValueError:
        print('FATAL ERROR: Connection closed')
        return
    game = userfunctions.start_game()
    while userfunctions.check_winner(game) is False:
        try:
            game = user_move(game, client)
            if userfunctions.check_winner(game) is True:
                break
            game = server_move(game, client)
        except ValueError:
            print('FATAL ERROR: Connection closed')
            break

    online.close_client(client)

if __name__ == '__main__':
    main()




ONLINE
import socket
import collections

Client = collections.namedtuple('Client',['connection','instream','outstream'])

def input_host()-> Client:
    '''
    Connects to server, creates i/o stream, and returns in a Client object
    Terminates if connection fails
    '''
    valid_port = False
    host = input('Host: ')
    while not valid_port:
        try:
            port = int(input('Port: '))
            valid_port = True
        except (ValueError,TypeError):
            print('ERROR: Invalid Port')
    client = socket.socket()
    try:
        client.connect((host,port))
        #client.connect(('woodhouse.ics.uci.edu',4444))
    except socket.gaierror:
        print('ERROR: Failed to get address info')
    except socket.timeout:
        print('ERROR: Timed out')
    except InterruptedError:
        print('ERROR: Connection interrupted')
    except ConnectionRefusedError:
        print('ERROR: Connection Refused')
    else:
        client_io = _create_io(client)
        return client_io

def ics_connect(client: Client):
    '''
    connects to woodhouse ics server with connect four protocol
    closes connection if invalid server response
    '''
    user = _input_username()
    msg = 'I32CFSP_HELLO ' + user
    _send_msg(client, msg)
    response = _recv_msg(client)
    if response != 'WELCOME ' + user:
        close_client(client)
    print('SERVER: ' + response)
    msg = 'AI_GAME'
    _send_msg(client, msg)
    response = _recv_msg(client)
    if response != 'READY':
        close_client(client)
    print('SERVER: ' + response)

def send_move(client: Client, col: int, move: int):
    '''
    sends move with correct syntax to server
    '''
    if move == 0:
        _send_msg(client,'POP ' + str(col))
    elif move == 1:
        _send_msg(client,'DROP ' + str(col))

def parse_msg(client: Client)->list:
    '''
    returns list of len 2
    1st element: -1 if invalid user move, 0-6 if server pop, 10-16 if server drop
    2nd element: -1 if bad input, 0 if ready, 1 if red win, 2 if yellow win
    '''
    msg_list = [0]*2
    msg = _recv_msg(client)
    print('SERVER: ' + msg)

    if msg == 'OKAY':
        move = _recv_msg(client)
        result = _recv_msg(client)
        print('SERVER: ' + move)
        print('SERVER: ' + result)
        #parse move and check if valid syntax
        if move[0:4] == 'POP ':
            try:
                msg_list[0] = int(move[-1]) - 1
            except (TypeError, ValueError, NameError):
                msg_list[1] = -1
        elif move[0:5] == 'DROP ':
            try:
                msg_list[0] = int(move[-1]) + 9
            except (TypeError, ValueError, NameError):
                msg_list[1] = -1
        else:
            msg_list[1] = -1

        #parse result and check if valid syntax
        if result.find('WINNER') != -1:
            if result == 'WINNER_RED':
                msg_list[1] = 1
            elif result == 'WINNER_YELLOW':
                msg_list[1] = 2
        elif result == 'READY':
            msg_list[1] = 0
        else:
            msg_list[1] = -1


    elif msg == 'INVALID':
        msg_list[0] = -1
        result = _recv_msg(client)
        print('SERVER: ' + result)
        if result == 'READY':
            msg_list[1] = 0
        else:
            msg_list[1] = -1


    else:
        msg_list[0] = -1
        msg_list[1] = -1
    #close sockets if bad move
    if msg_list[1] == -1:
        close_client(client)
    return msg_list

def _input_username()->str:
    valid = False
    user = str()
    while not valid:
        user = input('Enter Username: ')
        if user.find(' ') != -1 or len(user) == 0:
            print('ERROR: Invalid userame')
        else:
            valid = True
    return user

def _create_io(client: socket.socket)->Client:
    return Client(client,client.makefile('r'),client.makefile('w'))

def _send_msg(client: Client, msg: str):
    client.outstream.write(msg + '\r\n')
    client.outstream.flush()

def _recv_msg(client: Client)->str:
    return client.instream.readline()[:-1]

def close_client(client: Client)->str:
    client.instream.close()
    client.outstream.close()
    client.connection.close()



