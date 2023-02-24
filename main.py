
from game_Class import *

def main():
    pg.init()
    while True:
        game = Game()
        game.show_start_screen()
        game.start_game_loop()
        x = game.show_game_over_screen()
        if x == "end":
            break

    pg.quit()
    quit()

main()


