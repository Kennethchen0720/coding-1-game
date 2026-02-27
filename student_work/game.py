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

def draw_board(stdscr):
    
    # Print the board and all game elements using curses
    curses.start_color()

    # Make sure the terminal actually supports colors before trying to use them.  In a
    # few minimal environments (some CI containers, Windows without a proper terminal,
    # etc.) the curses color APIs raise "color matching" or "color number out of range"
    # errors.  Guard against that by falling back to A_NORMAL if colors aren't
    # available or initialization fails.
    color_attr = curses.A_NORMAL
    if curses.has_colors():
        try:
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_BLACK, -1)
            color_attr = curses.color_pair(1)
        except curses.error:
            # If the terminal doesn't like the -1 default background or the pair
            # number we chose, just continue with the default attributes.  The game
            # will still display.
            color_attr = curses.A_NORMAL

    stdscr.clear()

    # determine how much space we actually have; curses will return ERR if we
    # try to draw outside the window (which is what happened in the screenshot).
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

        # only attempt to draw if the target row is within the visible area
        if y < max_y - 2:
            try:
                # use addnstr to avoid overflow if row is wider than the screen
                stdscr.addnstr(y, 0, row, max_x, color_attr)
            except curses.error:
                # if drawing still fails (e.g. cell width mismatch), just skip it
                pass

    # draw status lines safely near the bottom of the screen
    info_y = min(game_data['height'], max_y - 2)
    try:
        stdscr.addnstr(info_y, 0,
                       f"Coins Collected: {game_data['player']['score']}",
                       max_x, color_attr)
    except curses.error:
        pass
    try:
        stdscr.addnstr(info_y + 1, 0,
                       "Move with A/D, Q to quit",
                       max_x, color_attr)
    except curses.error:
        pass
    stdscr.refresh()

    


def move_player(key):
    x = game_data['player']['x']
    y = game_data['player']['y']
    new_x, new_y = x, y
    key = key.lower()

    if key == "a":
        new_x -= 1
    elif key == "d":
        new_x += 1
    else:
        return

    # bounds check
    if not (0 <= new_x < game_data['width'] and 0 <= new_y < game_data['height']):
        return

    # Check for obstacles (safe access)
    for o in game_data.get('obstacles', []):
        if o.get('x') == new_x and o.get('y') == new_y:
            return

    # move player
    game_data['player']['x'] = new_x
    game_data['player']['y'] = new_y

    # collect coins
    for c in game_data.get('collectibles', []):
        if not c.get('collected') and c.get('x') == new_x and c.get('y') == new_y:
            c['collected'] = True
            game_data['player']['score'] += 1

    # bomb collision
    bp = game_data.get('bomb_pos', {})
    if bp.get('x') == new_x and bp.get('y') == new_y:
        game_data['player']['lives'] -= 1

def bomb_and_coin_fall():
    x = random.randint(0, game_data['width'] - 1)
    b_or_c = random.randint(0, 5)
    if b_or_c == 5:
        game_data['bomb_pos'] = {"x": x, "y": 20}
    else:
        game_data['collectibles'] = {"x": x, "y": 20, "collected": False}

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    draw_board(stdscr)
    current_time = 0

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
        
        if current_time % 3 == 0:
            bomb_and_coin_fall()
        current_time += 1

curses.wrapper(main)