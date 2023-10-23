
from source import tools
from source.states import main_menu, load_screen_1, game_screen_1, results, load_screen_2, game_screen_2


def main():

    state_dict = {
        'main_menu': main_menu.MainMenu(),
        'load_screen_1': load_screen_1.LoadScreen(),
        'load_screen_2': load_screen_2.LoadScreen(),
        'game_screen_1': game_screen_1.GameScreen(),
        'game_screen_2': game_screen_2.GameScreen(),
        'results': results.Results()
    }
    game = tools.Game(state_dict, 'main_menu')
    game.run()


if __name__ == '__main__':
    main()
