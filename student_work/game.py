# Write your game here
import curses
import random 
import time

game_data = {
    'width': 12,
    'height': 20,
    'player': {"x":5, "y":10, "score":0, "lives":3},
    'bomb_pos': {"x":1,"y":1},
    'collectibles':[{"x": 10, "y": 5, "collected": False}],
    'obstacles': [],
    'coins': "\U0001FA99",
    'bomb': "\U0001F4A3",
    'Basket': "\U0001F5D1",
    'empty': "  "
}

def display_welcome_screen():
    print(" ")
    print("Welcome to Basket Catcher!")
    print(" ")
    print("Use AD for movement")
    print("Avoid the Bomb")
    print("Collect Coins!")


def draw_board(stdscr):
    curses.start_color()
    color_attr = curses.A_NORMAL
    if curses.has_colors():
        try:
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_BLACK, -1)
            color_attr = curses.color_pair(1)
        except curses.error:
            color_attr = curses.A_NORMAL

    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()

    for y in range(game_data['height']):
        row = ""
        for x in range(game_data['width']):
            # Player
            if x == game_data['player']['x'] and y == game_data['player']['y']:
                row += game_data['Basket']
            # Bomb
            elif x == game_data['bomb_pos']['x'] and y == game_data['bomb_pos']['y']:
                row += game_data['bomb']
            #  Coins
            x = random.randint(0, game_data['width'] - 1)
            b_or_c = random.randint(0, 5)
            if b_or_c == 5:
                game_data['bomb_pos'] = {"x": x, "y": 19}
                row += game_data['bomb']
            elif:
                game_data['collectibles'] = {"x": x, "y": 20, "collected": False}
                row += game_data['coins']
            elif any(c['x'] == x and c['y'] == y and not c['collected'] for c in game_data['collectibles']):
                row += game_data['coins']
            else:
                row += game_data['empty']


   