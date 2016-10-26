import connectfour
import userfunctions
import online
'''
def user_move(game: connectfour.GameState, client: online.Client)-> connectfour.GameState:
    '''
    #makes a move in the client-side game board and sends the move to the server
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
    #Accepts a move from the server and updates it in the client side game board
'''
    move = online.parse_msg(client)
    if move[1] >= 0:
        if move[0] < 10 and move[0] >= 0:
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
            return game
'''


def update_game(game: connectfour.GameState, client: online.Client)-> connectfour.GameState:
    '''
    Asks for user input and sends to server
    Receives server input
    Handles user and server input and returns updated gamestate
    Combined user_move and server_move to allow for consistent UI after game ends
    '''


    #Input user move and send to server
    move = userfunctions.get_move()
    col = userfunctions.int_input()
    online.send_move(client, col + 1, move)#add 1 because int_input subtracts 1
    #receive response from server
    response = online.parse_msg(client)
    #handle user move
    if move == 0:
        print('USER: Pop at column ' + str(col + 1))
        game = userfunctions.catch_pop(game, col)
    elif move == 1:
        print('USER: Drop at column ' + str(col + 1))
        game = userfunctions.catch_drop(game, col)
    userfunctions.display_board(game)
    #Handle server move
    if response[2] >= 0:
        if response[0] == 1:
            print('SERVER: Pop at column ' + str(response[1] + 1))
            game = userfunctions.catch_pop(game, response[1])
            userfunctions.display_board(game)
        elif response[0] == 2:
            print('SERVER: Drop at column ' + str(response[1] + 1))
            game = userfunctions.catch_drop(game, response[1])
            userfunctions.display_board(game)
        
        elif response[0] == -1:
            if game.turn != connectfour.RED:#checks to see if server has made a move after a valid user move
                print('FATAL ERROR: Bad server')
                online.close_client(client)
                return #returns none, indicates client/server desync
        #if game is ended
        if response[2] == 1:
            print('GAME OVER: Red Wins')
        elif response[2] == 2:
            print('GAME OVER: Yellow Wins')
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
    while userfunctions.check_winner(game,True) is False:
        try:
            #game = user_move(game, client)
            #game = server_move(game, client)
            game = update_game(game, client)


            if game == None: #client desynced with server
                return
        except ValueError:
            print('FATAL ERROR: Connection closed')
            break


    online.close_client(client)


if __name__ == '__main__':
    main()






