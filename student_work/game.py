import curses
import time
import random


game_data = {
    'width': 15,
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
    print("Use A/D for movement")
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
            # Coins
            elif any(c['x'] == x and c['y'] == y and not c['collected'] for c in game_data['collectibles']):
                row += game_data['coins']
            else:
                row += game_data['empty']

        if y < max_y - 2:
            try:
                stdscr.addnstr(y, 0, row, max_x, color_attr)
            except curses.error:
                pass


    info_y = min(game_data['height'], max_y - 2)
    try:
        stdscr.addnstr(info_y, 0,
                       f"Coins Collected: {game_data['player']['score']}",
                       max_x, color_attr)
    except curses.error:
        pass
    try:
        stdscr.addnstr(info_y + 1, 0,
                       "Move with A/D Q to quit",
                       max_x, color_attr)
    except curses.error:
        pass
    stdscr.refresh()

def move_player(key):
    x = game_data['player']['x']
    new_x = x
    key = key.lower()

    if key == "a":
        new_x -= 1
    elif key == "d":
        new_x += 1
    else:
        return

    # bounds check
    if not (0 <= new_x < game_data['width']):
        return

    # Check for obstacles (safe access)
    for o in game_data.get('obstacles', []):
        if o.get('x') == new_x:
            return

    # move player
    game_data['player']['x'] = new_x


def spawn_coin():
    # Limit number of leaves on board
    active_coins = [c for c in game_data['collectibles'] if not c["collected"]]
    if len(active_coins) >= 3:
        return

    if random.random() > 0.5:
        return

    while True:
        x = random.randint(0, game_data['width'] - 1)
        y = random.randint(0, game_data['height'] - 1)

        # Must not spawn on player, eagle, rock, or existing leaf
        if (x == game_data['player']["x"] and y == game_data['player']["y"]):
            continue

        if (x == game_data['bomb_pos']["x"] and y == game_data['bomb_pos']["y"]):
            continue

        if any(c["x"] == x and c["y"] == y and not c["collected"]
               for c in game_data['collectibles']):
            continue

        # Valid location found
        game_data['collectibles'].append({
            "x": x,
            "y": y,
            "collected": False
        })
        break

    # collect coins
    for c in game_data.get('collectibles', []):
        if not c.get('collected') and c.get('x') == new_x :
            c['collected'] = True
            game_data['player']['score'] += 1

    # bomb collision
    bp = game_data.get('bomb_pos', {})
    if bp.get('x') == new_x:
        game_data['player']['lives'] -= 1


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    draw_board(stdscr)

    while True:
        try:
            key = stdscr.getkey()
        except curses.error:
            key = None

        if key:
            if key.lower() == "q":
                break

            move_player(key)
            draw_board(stdscr)



    stdscr.clear()
    stdscr.addstr(2, 2, "GAME OVER")
    stdscr.addstr(3, 2, f"Final Score (Coin Collected): {game_data['player']['score']}")
    stdscr.refresh()
    time.sleep(3)

display_welcome_screen()
time.sleep(3.0)
curses.wrapper(main)