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

# coordiante n = current_position[n]
original_board = [0] * 266
current_board = [0] * 266
highlight = [0] * 266

key_lock = False
enter_lock = False
moves = 1


def setup():
    global temp_rack, original_board

    py5.size(1500, 1500)
    py5.text_size(60)
    py5.background('#000000')

    scrabble.gen_tiles(player1, scrabble.tile_bag)
    scrabble.gen_tiles(player2, scrabble.tile_bag)

    temp_rack = player1.copy()
    original_board = current_board.copy()


def draw():
    global moves

    board()

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
        py5.fill("#EBB36F")
        py5.square(x, y, 50)

        py5.fill('#FFFFFF')
        py5.text(box, x + 5, y + 45)

        x += 60


# highlight the selected cell
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
    global key_lock, enter_lock, moves
    global player1_score, player2_score
    global temp_rack, original_board, inuse, highlight

    if py5.is_key_pressed:
        key = py5.key.upper()

        # arrow keys (movement)
        if py5.key == py5.CODED:
            if not key_lock:
                if 1 in highlight:
                    square = highlight.index(1)
                    movement(square)
                key_lock = True
            return

        # placing letters
        if key in tiles:
            if 1 in highlight and key in temp_rack:
                pos = highlight.index(1)

                # can't overwrite locked tiles
                if original_board[pos] not in (0, 1):
                    return

                # if replacing a tile placed this turn
                if current_board[pos] not in (0, 1):
                    old = current_board[pos]
                    inuse.remove(old)
                    temp_rack.append(old)

                current_board[pos] = key
                inuse.append(key)
                temp_rack.remove(key)

        # --- BACKSPACE removes a tile placed this turn ---
        if py5.key == py5.BACKSPACE:
            if 1 in highlight:
                pos = highlight.index(1)

                # only remove tiles placed THIS turn
                if current_board[pos] in inuse:
                    removed = current_board[pos]

                    # clear the board square
                    current_board[pos] = 0

                    # return tile to temp rack
                    temp_rack.append(removed)

                    # remove from inuse list
                    inuse.remove(removed)

            return

        # submitting the move
        if py5.key in ("RETURN", "\n"):
            if not enter_lock:
                enter_lock = True

                if validation.valid(current_board):

                    # 1. score the move
                    points = scoring.score_move(original_board, current_board)

                    if moves % 2 == 1:
                        player1_score += points
                    else:
                        player2_score += points

                    print(player1_score)
                    print(player2_score)
                    # 2. remove used tiles from current player's rack
                    for t in inuse:
                        if t in tiles:
                            tiles.remove(t)

                    # 3. lock in board for next turn
                    original_board = current_board.copy()

                    # 4. switch player
                    moves += 1

                    # 5. reset temp_rack for next player
                    if moves % 2 == 1:
                        temp_rack = player1.copy()
                    else:
                        temp_rack = player2.copy()

                    # 6. reset highlight + inuse
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

    # ensure temp_rack matches current player at start of their turn
    if not inuse:
        if temp_rack != player:
            temp_rack = player.copy()

    show_tiles(player)
    click()
    letter_enter(player)
    show_board()


py5.run_sketch()
