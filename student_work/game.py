# Write your game here
import curses

game_data = {
    'width': 10,
    'height': 20,
    'player': {"x":0, "y":0, "score":0, "lives":3, "max_lives":3}
    'bomb_pos':{"x":1,"y":1}
    'collectibles': [
        {"x": 5, "y": 20, "collected": False},
    ]

    #Emoji
    'coins': "🪙"
    'bomb': "💣"
    'Basket': "👛"
    'empty': "  "
}

def draw_board(screen):
    
    # Print the board and all game elements using curses
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)

    screen.clear()
    for y in range(game_data['height']):
        row = ""
        for x in range(game_data['width']):
            # Player
            if x == game_data['player']['x'] and y == game_data['player']['y']:
                row += game_data['Basket']
            # Eagle
            elif x == game_data['bomb_pos']['x'] and y == game_data['bomb_pos']['y']:
                row += game_data['bomb']
            # Collectibles
            elif any(c['x'] == x and c['y'] == y and not c['collected'] for c in game_data['collectibles']):
                row += game_data['coins']
            else:
                row += game_data['empty']
        screen.addstr(y, 0, row, curses.color_pair(1))

    screen.refresh()
    screen.getkey()  # pause so player can see board

curses.wrapper(draw_board)



# Good Luck!