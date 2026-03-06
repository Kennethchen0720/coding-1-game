import threading
import time
import curses
import random

game_data = {
    'width': 10,
    'height': 20,
    'player': {"x":5, "y":10, "score":0, "lives":2},
    'bombs': [{"x":1,"y":1}], # List of bombs, each with x, y
    'collectibles':[{"x": 5, "y": 5, "collected": False}],
    'obstacles': [],
    'coins': "\U0001FA99",
    'bomb': "\U0001F4A3",
    'Basket': "\U0001F5D1",
    'empty': "  ",
    'bomb_timer': 0,
    'coin_timer': 0
}
#this is what you would see in the start menu
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
            curses.init_pair(1, curses.COLOR_BLACK, - 1)
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
            elif any(b['x'] == x and b['y'] == y for b in game_data['bombs']):
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


    #Display score and lives
    try:
        stdscr.addnstr(info_y, 0,
                       f"Coins Collected: {game_data['player']['score']}",
                       max_x, color_attr)
    except curses.error:
        pass
    try:
        stdscr.addnstr(info_y + 1, 0,
                       f"Lives Remaining: {game_data['player']['lives']}",
                       max_x, color_attr)
    except curses.error:
        pass
    stdscr.refresh()
#This is how you would move the player left and right using the A and D keys
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

    # bounds check so you won't go off the board
    if not (0 <= new_x < game_data['width']):
        return

    # Check for obstacles (safe access)
    for o in game_data.get('obstacles', []):
        if o.get('x') == new_x:
            return

    # move player
    game_data['player']['x'] = new_x

    # Check for bomb collision
    for b in game_data.get('bombs', []):
        if b['x'] == game_data['player']['x'] and b['y'] == game_data['player']['y']:
            game_data['player']['lives'] -= 1

    return True

def update_game_objects():
    # Move coins down
    for c in game_data['collectibles']:
        if not c['collected']:
            c['y'] += 1
            if c['y'] >= game_data['height']:
                c['collected'] = True  # Remove coin when it falls off the board
    
    # Move bombs down
    for b in game_data['bombs']:
        b['y'] += 1
        if b['y'] >= game_data['height']:
            game_data['bombs'].remove(b)  # Remove bomb when it falls off
    
    # Check for collection at player's position
    player_x = game_data['player']['x']
    player_y = game_data['player']['y']
    for c in game_data['collectibles']:
        if not c['collected'] and c['x'] == player_x and c['y'] == player_y:
            c['collected'] = True
            game_data['player']['score'] += 1
    for b in game_data['bombs']:
        if b['x'] == player_x and b['y'] == player_y:
            game_data['player']['lives'] -= 1
            game_data['bombs'].remove(b) 
         # Remove bomb on collision

def spawn_bomb():
    game_data['bomb_timer'] += 1
    if game_data['bomb_timer'] % 2 == 0:  # Spawn bomb every 5 frames
        if random.random() > 0.5:  #20% spawn bomb
            return

        # Limit number of bombs on board
        active_bombs = [b for b in game_data['bombs']]
        if len(active_bombs) >= random.randint(1, 6):
            return


        while True:
            x = random.randint(0, game_data['width'] - 1)
            y = 0  # Spawn at the top

            # Must not spawn on player
            if (x == game_data['player']["x"] and y == game_data['player']["y"]):
                continue

            # Valid location found
            game_data['bombs'].append({
                "x": x,
                "y": y
            })
            break
    else:
        return

def spawn_coin():
    game_data['coin_timer'] += 1
    if game_data['coin_timer'] % 2 == 0:  # Spawn coin
        if random.random() > 0.8: #80% spawn coin
            return

        # Limit number of coins on board
        active_coins = [c for c in game_data['collectibles'] if not c["collected"]]
        if len(active_coins) >= random.randint(1, 9):
            return


        while True:
            x = random.randint(0, game_data['width'] - 1)
            y = 0  # Spawn at the top

            # Must not spawn on player or bomb
            if (x == game_data['player']["x"] and y == game_data['player']["y"]):
                continue

            if any(b["x"] == x and b["y"] == y for b in game_data['bombs']):
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
    else:
        return

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    draw_board(stdscr)

    frame_count = 0

    while True:
        try:
            key = stdscr.getkey()
        except curses.error:
            key = None

    #If you want to quit than press q to be in the end screen
        if key:
            if key.lower() == "q":
                break

            move_player(key)
    #If you lose all your lives than the game will end and you will be in the end screen
        if len(game_data['bombs']) > 0 and game_data['player']['lives'] <= 0:
            break


        # Update game objects every few frames
        if frame_count % 4 == 0:
            update_game_objects()
            spawn_bomb()
            spawn_coin()

        draw_board(stdscr)
        time.sleep(0.05)
        frame_count += 1 



    stdscr.clear()
    stdscr.addstr(2, 2, "GAME OVER")
    stdscr.addstr(3, 2, f"Final Score (Coin Collected): {game_data['player']['score']}")
    stdscr.refresh()
    time.sleep(3)

display_welcome_screen()
time.sleep(3.0)
curses.wrapper(main)