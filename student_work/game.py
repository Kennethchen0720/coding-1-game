# Write your game here
import curses

game_data = {
    'width': 40,
    'height': 40,
    'player': {"x":5, "y":10, "score":0, "lives":3},
    'bomb_pos': {"x":1,"y":1},
    'collectibles':[{"x": 10, "y": 5, "collected": False}],
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
        if y < max_y:
            try:
                # use addnstr to avoid overflow if row is wider than the screen
                stdscr.addnstr(y, 0, row, max_x, color_attr)
            except curses.error:
                # if drawing still fails (e.g. cell width mismatch), just skip it
                pass

    stdscr.refresh()
    stdscr.getkey()  # pause so player can see board

curses.wrapper(draw_board)

def move_player(key):
    x = game_data['player']['x']

    new_x = x
    key = key.lower()


    if key == "a" and x > 0:
        new_x -= 1
    elif key == "d" and x < game_data['width'] - 1:
        new_x += 1
    else:
        return  # Invalid key or move off board

    # Check for obstacles
    if any(o['x'] == new_x and o['y'] == new_y for o in game_data['obstacles']):
        return

    # Update position and increment score
    game_data['player']['x'] = new_x
    game_data['player']['y'] = new_y
    game_data['player']['score'] += 1

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    draw_board(stdscr)

    while True:
        try:
            key = stdscr.getkey()
        except:
            key = None

        if key:
            if key.lower() == "q":
                break

            move_player(key)
            draw_board(stdscr)

curses.wrapper(main)
# Good Luck!