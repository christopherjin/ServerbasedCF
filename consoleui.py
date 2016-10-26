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
