import py5
import scrabble
import validation
import scoring

# special tile co-ordinates
TRIP_WORDS = [1,8,15,106,120,211,218,225]
DOUB_WORDS = [17,29,33,43,49,57,65,71,113,155,161,169,177,183,193,197,209]
TRIP_LETTERS = [21,25,77,81,85,89,137,141,145,149,201,205]
DOUB_LETTERS = [4,12,37,39,46,53,60,93,97,99,103,109,117,123,127,129,133,166,173,180,187,189,214,222]

# player racks
player1 = []
player2 = []
player1_score = 0
player2_score = 0

inuse = []
temp_rack = []

# coordinate n = current_position[n]
original_board = [0] * 266
current_board = [0] * 266
highlight = [0] * 266

key_lock = False
enter_lock = False
moves = 1

# --- Exchange state ---
exchange_mode = False   # True when player is picking tiles to exchange
exchange_tiles = []     # tiles queued up for exchange


def setup():
    global temp_rack, original_board

    py5.size(1500, 1500)
    py5.text_size(50)
    py5.background('#000000')

    scrabble.gen_tiles(player1, scrabble.tile_bag)
    scrabble.gen_tiles(player2, scrabble.tile_bag)

    temp_rack = player1.copy()
    original_board = current_board.copy()


def draw():
    global moves

    py5.background('#000000')
    board()
    show_scores()
    show_exchange_status()

    if moves % 2 == 1:
        turns(player1)
    else:
        turns(player2)


def board():
    box = 1
    x = 10
    y = 10

    while box < 226:
        if box in TRIP_WORDS:
            py5.fill("#9D0606")
        elif box in DOUB_WORDS:
            py5.fill("#FCC93F")
        elif box in TRIP_LETTERS:
            py5.fill("#065FCC")
        elif box in DOUB_LETTERS:
            py5.fill("#39CBEC")
        else:
            py5.fill("#0B762B")

        py5.square(x, y, 50)

        if box % 15 == 0:
            x = 10
            y += 60
        else:
            x += 60

        box += 1


def show_tiles(tiles):
    x = 1000
    y = 250

    for box in tiles:
        # highlight tiles queued for exchange in red
        if exchange_mode and box in exchange_tiles:
            py5.fill("#CC3300")
        else:
            py5.fill("#EBB36F")
        py5.square(x, y, 50)

        py5.fill('#FFFFFF')
        py5.text(box, x + 5, y + 45)

        x += 60


def show_exchange_status():
    """Show a status line when exchange mode is active."""
    if not exchange_mode:
        return

    py5.text_size(35)
    py5.fill("#CC3300")
    py5.rect(950, 160, 500, 50)
    py5.fill('#FFFFFF')

    if exchange_tiles:
        py5.text("SWAP: " + " ".join(exchange_tiles) + "  (/ confirm)", 960, 196)
    else:
        py5.text("Type tiles to swap, / confirm", 960, 196)

    py5.text_size(50)


def click():
    if py5.is_mouse_pressed:
        x = py5.mouse_x
        y = py5.mouse_y

        col = (x // 60) + 1
        row = (y // 60)
        pos = row * 15 + col

        if pos < 1 or pos > 225:
            return

        if 1 in highlight:
            highlight[highlight.index(1)] = 0

        highlight[pos] = 1


def letter_enter(tiles):
    global key_lock, enter_lock, moves, exchange_mode, exchange_tiles
    global player1_score, player2_score
    global temp_rack, original_board, inuse, highlight

    if py5.is_key_pressed:
        key = py5.key.upper()

        # --- Irish vowel shortcuts ---
        special_map = {
            '3': 'Á',
            '4': 'É',
            '5': 'Í',
            '6': 'Ó',
            '7': 'Ú'
        }
        if key in special_map:
            key = special_map[key]

        # --- EXCHANGE MODE: toggle on first /, confirm on second / ---
        if py5.key == '/':
            if not key_lock:
                key_lock = True

                if not exchange_mode:
                    # Enter exchange mode (only allowed if no tiles on board yet)
                    if not inuse:
                        exchange_mode = True
                        exchange_tiles = []
                        print("Exchange mode ON – type tiles, press / to confirm, # to cancel")
                else:
                    # Confirm the exchange
                    if exchange_tiles and len(scrabble.tile_bag) > 0:
                        import random
                        player = player1 if moves % 2 == 1 else player2

                        for t in exchange_tiles:
                            if t in player:
                                player.remove(t)

                        for t in exchange_tiles:
                            pos = random.randint(0, len(scrabble.tile_bag))
                            scrabble.tile_bag.insert(pos, t)

                        scrabble.gen_tiles(player, scrabble.tile_bag)
                        print("Exchanged:", exchange_tiles)

                        moves += 1
                        original_board = current_board.copy()

                        if moves % 2 == 1:
                            temp_rack = player1.copy()
                        else:
                            temp_rack = player2.copy()

                        highlight = [0] * 266
                        inuse = []

                    elif len(scrabble.tile_bag) == 0:
                        print("Bag empty – cannot exchange")

                    exchange_mode = False
                    exchange_tiles = []

            return

        # --- # cancels exchange mode, or passes turn normally ---
        if key == '#':
            if not key_lock:
                key_lock = True

                if exchange_mode:
                    exchange_mode = False
                    exchange_tiles = []
                    print("Exchange cancelled")
                else:
                    moves += 1
                    original_board = current_board.copy()

                    if moves % 2 == 1:
                        temp_rack = player1.copy()
                    else:
                        temp_rack = player2.copy()

                    highlight = [0] * 266
                    inuse = []
                    print("PASS")

            return

        # --- BACKSPACE: remove last queued tile in exchange mode, else normal ---
        if py5.key == py5.BACKSPACE:
            if exchange_mode:
                if exchange_tiles:
                    exchange_tiles.pop()
                return

            if 1 in highlight:
                pos = highlight.index(1)
                if current_board[pos] in inuse:
                    removed = current_board[pos]
                    current_board[pos] = 0
                    temp_rack.append(removed)
                    inuse.remove(removed)
            return

        # --- In exchange mode: typing a letter queues it ---
        if exchange_mode:
            if not key_lock:
                key_lock = True
                if (key in tiles
                        and len(exchange_tiles) < 7
                        and exchange_tiles.count(key) < tiles.count(key)):
                    exchange_tiles.append(key)
            return

        # --- Normal play ---

        if py5.key == py5.CODED:
            if not key_lock:
                if 1 in highlight:
                    square = highlight.index(1)
                    movement(square)
                key_lock = True
            return

        if key in tiles:
            if 1 in highlight and key in temp_rack:
                pos = highlight.index(1)

                if original_board[pos] not in (0, 1):
                    return

                if current_board[pos] not in (0, 1):
                    old = current_board[pos]
                    inuse.remove(old)
                    temp_rack.append(old)

                current_board[pos] = key
                inuse.append(key)
                temp_rack.remove(key)

        if py5.key in ("RETURN", "\n"):
            if not enter_lock:
                enter_lock = True

                if validation.valid(current_board, original_board):

                    points = scoring.score_move(original_board, current_board)

                    if moves % 2 == 1:
                        player1_score += points
                    else:
                        player2_score += points

                    for t in inuse:
                        if t in tiles:
                            tiles.remove(t)

                    original_board = current_board.copy()
                    moves += 1

                    if moves % 2 == 1:
                        temp_rack = player1.copy()
                    else:
                        temp_rack = player2.copy()

                    highlight = [0] * 266
                    inuse = []

            return


def show_board():
    box = 1
    x = 10
    y = 10

    while box < 226:
        if current_board[box] not in (0, 1):
            py5.fill('#FFFFFF')
            py5.text(current_board[box], x + 5, y + 45)

        if highlight[box] == 1:
            py5.no_fill()
            py5.stroke("#d7b015")
            py5.stroke_weight(5)
            py5.rect(x + 2.5, y + 2.5, 45, 45)
            py5.no_stroke()

        if box % 15 == 0:
            x = 10
            y += 60
        else:
            x += 60

        box += 1


def movement(square):
    if py5.key_code == py5.UP:
        if square < 16:
            square = 225 - (15 - square)
        else:
            square -= 15
    elif py5.key_code == py5.DOWN:
        if square > 210:
            square -= 210
        else:
            square += 15
    elif py5.key_code == py5.LEFT:
        if square == 1:
            square = 225
        else:
            square -= 1
    elif py5.key_code == py5.RIGHT:
        if square == 225:
            square = 1
        else:
            square += 1

    if 1 in highlight:
        highlight[highlight.index(1)] = 0
    highlight[square] = 1


def key_released():
    global key_lock, enter_lock
    key_lock = False
    enter_lock = False


def turns(player):
    global temp_rack

    if (len(player) < 7) and (len(scrabble.tile_bag) != 0):
        scrabble.gen_tiles(player, scrabble.tile_bag)

    if not inuse and not exchange_mode:
        if temp_rack != player:
            temp_rack = player.copy()

    show_tiles(temp_rack)
    click()
    letter_enter(player)
    show_board()


def show_scores():
    global player1_score, player2_score

    py5.fill("#0CAB07")
    py5.rect(950, 10, 500, 50)
    py5.fill("#3d10f5")
    py5.rect(950, 60, 500, 50)

    py5.fill('#000000')
    py5.text(player1_score, 1175, 55)
    py5.text(player2_score, 1175, 105)


py5.run_sketch()