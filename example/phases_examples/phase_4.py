# The goals for this phase include:
# - Add Enemies / Collectibles to the board
# - Movement or spawn logic is applied
# - Board updates display changes after each move.

import curses
import random
import time

game_data = {
    'width': 5,
    'height': 5,
    'player': {"x": 0, "y": 0, "score": 0, "energy": 10, "max_energy": 10},
    'eagle_pos': {"x": 4, "y": 4},
    'collectibles': [
        {"x": 2, "y": 1, "collected": False},
    ],
    'obstacles': [
        {"x": 1, "y": 2},
        {"x": 3, "y": 1}
    ],

    # ASCII icons
    'turtle': "\U0001F422",
    'eagle_icon': "\U0001F985",
    'obstacle': "\U0001FAA8 ",
    'leaf': "\U0001F343",
    'empty': "  "
}

def draw_board(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)

    stdscr.clear()
    for y in range(game_data['height']):
        row = ""
        for x in range(game_data['width']):
            # Player
            if x == game_data['player']['x'] and y == game_data['player']['y']:
                row += game_data['turtle']
            # Eagle
            elif x == game_data['eagle_pos']['x'] and y == game_data['eagle_pos']['y']:
                row += game_data['eagle_icon']
            # Obstacles
            elif any(o['x'] == x and o['y'] == y for o in game_data['obstacles']):
                row += game_data['obstacle']
            # Collectibles
            elif any(c['x'] == x and c['y'] == y and not c['collected'] for c in game_data['collectibles']):
                row += game_data['leaf']
            else:
                row += game_data['empty']
        stdscr.addstr(y, 0, row, curses.color_pair(1))

    stdscr.refresh()

def move_player(key):
    x = game_data['player']['x']
    y = game_data['player']['y']
    new_x, new_y = x, y
    key = key.lower()

    if key == "w" and y > 0:
        new_y -= 1
    elif key == "s" and y < game_data['height'] - 1:
        new_y += 1
    elif key == "a" and x > 0:
        new_x -= 1
    elif key == "d" and x < game_data['width'] - 1:
        new_x += 1

    game_data['player']['x'] = new_x
    game_data['player']['y'] = new_y

def move_eagle():
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    random.shuffle(directions)
    ex, ey = game_data['eagle_pos']['x'], game_data['eagle_pos']['y']

    for dx, dy in directions:
        new_x = ex + dx
        new_y = ey + dy
        if 0 <= new_x < game_data['width'] and 0 <= new_y < game_data['height']:
            if not any(o['x'] == new_x and o['y'] == new_y for o in game_data['obstacles']):
                game_data['eagle_pos']['x'] = new_x
                game_data['eagle_pos']['y'] = new_y
                break

def spawn_leaf():
    active_leaves = [c for c in game_data['collectibles'] if not c['collected']]
    if len(active_leaves) >= 3:
        return
    if random.random() > 0.2:
        return

    while True:
        x = random.randint(0, game_data['width'] - 1)
        y = random.randint(0, game_data['height'] - 1)

        if (x, y) == (game_data['player']['x'], game_data['player']['y']):
            continue
        if (x, y) == (game_data['eagle_pos']['x'], game_data['eagle_pos']['y']):
            continue
        if any(o['x'] == x and o['y'] == y for o in game_data['obstacles']):
            continue
        if any(c['x'] == x and c['y'] == y and not c['collected'] for c in game_data['collectibles']):
            continue

        game_data['collectibles'].append({"x": x, "y": y, "collected": False})
        break

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
            time.sleep(0.2)

curses.wrapper(main)