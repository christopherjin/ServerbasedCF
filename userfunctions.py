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
    result = int()
    valid = False
    while not valid:
        try:
            result = int(input('Select a column (1-'+ str(connectfour.BOARD_COLUMNS) + '): '))
            if result not in range(1,connectfour.BOARD_COLUMNS + 1):
                print('ERROR: Invalid Column')
            else:
                valid = True
        except (TypeError, ValueError):
            print('ERROR: Invalid Input')


    return result - 1#connect four library functions are 0-indexed


def display_board(game: connectfour.GameState):


    '''Displays current board when called'''
    col_array = game.board
    for n in range(1, connectfour.BOARD_COLUMNS+1): #display col #s
        print(n, end=' ')
    print()
    for i in range(0, connectfour.BOARD_ROWS): #displays board
        for col in col_array:
            if col[i] == connectfour.NONE:
                print('.', end=' ')
            elif col[i] == connectfour.RED:
                print('R', end=' ')
            elif col[i] == connectfour.YELLOW:
                print('Y', end=' ')
        print()


def get_move()->int:
    '''
    Asks user for choice of move
    '''
    valid = False
    while not valid:
        move = input('Pop or Drop? (P/D)').upper()
        if move == 'P':
            return 0
        elif move == 'D':
            return 1
        else:
            print('ERROR: Invalid Input')
            


def check_winner(game: connectfour.GameState, server=False)->bool:
    '''
    Checks for a winner in the current gamestate by trying to drop in a column
    '''
    try:
        for i in range(0,connectfour.BOARD_COLUMNS):
            try:
                connectfour.drop(game, i) #try to drop a piece in current gamestate
            except connectfour.InvalidMoveError:
                pass
        return False
    except connectfour.GameOverError:
        winner = connectfour.winner(game)
        if not server:
            print('Game Over')
            if winner == connectfour.RED:
                print('Red Wins')
            elif winner == connectfour.YELLOW:
                print('Yellow Wins')
        return True














