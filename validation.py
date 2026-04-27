# Load dictionary
with open('irish_dictionary.txt', 'r', encoding='utf-8', errors='replace') as data:
    words = data.read().splitlines()


# ---------------------------------------------------------
#  BLANK TILE SUPPORT
# ---------------------------------------------------------

def word_matches_with_blanks(word, dictionary):
    """
    Returns True if the word is valid, allowing '?' to match ANY letter.
    Supports multiple blanks and Irish accented vowels.
    """

    # No blanks → normal check
    if '?' not in word:
        return word in dictionary

    # All possible letters (A–Z + Irish vowels)
    from string import ascii_uppercase
    letters = list(ascii_uppercase) + ['Á', 'É', 'Í', 'Ó', 'Ú']

    # Build all possible substitutions
    possibilities = ['']
    for ch in word:
        if ch == '?':
            possibilities = [p + l for p in possibilities for l in letters]
        else:
            possibilities = [p + ch for p in possibilities]

    # Accept if ANY valid word exists
    return any(p in dictionary for p in possibilities)


# ---------------------------------------------------------
#  HELPER: is a board position occupied?
# ---------------------------------------------------------

def is_tile(board, pos):
    return board[pos] not in (0, 1)


# ---------------------------------------------------------
#  CONNECTIVITY CHECK (flood fill)
#  All tiles on the board must form one connected group.
# ---------------------------------------------------------

def all_connected(board):
    # Collect every occupied position
    occupied = [pos for pos in range(1, 226) if is_tile(board, pos)]
    if not occupied:
        return True

    # Flood fill from the first tile
    visited = set()
    stack = [occupied[0]]
    while stack:
        pos = stack.pop()
        if pos in visited:
            continue
        visited.add(pos)
        row = (pos - 1) // 15
        col = (pos - 1) % 15
        # up
        if row > 0 and is_tile(board, pos - 15):
            stack.append(pos - 15)
        # down
        if row < 14 and is_tile(board, pos + 15):
            stack.append(pos + 15)
        # left
        if col > 0 and is_tile(board, pos - 1):
            stack.append(pos - 1)
        # right
        if col < 14 and is_tile(board, pos + 1):
            stack.append(pos + 1)

    if len(visited) != len(occupied):
        print("Disconnected tiles on board")
        return False
    return True


# ---------------------------------------------------------
#  STRAIGHT LINE CHECK
#  New tiles must all be in the same row OR same column,
#  and there must be no empty gaps between them.
# ---------------------------------------------------------

def in_straight_line(new_tiles, board):
    if len(new_tiles) <= 1:
        return True

    rows = [(pos - 1) // 15 for pos in new_tiles]
    cols = [(pos - 1) % 15 for pos in new_tiles]

    if len(set(rows)) == 1:
        # All in same row — check no empty gaps between min and max col
        r = rows[0]
        for c in range(min(cols), max(cols) + 1):
            pos = r * 15 + c + 1
            if not is_tile(board, pos):
                print("Gap in row placement")
                return False
        return True

    if len(set(cols)) == 1:
        # All in same column — check no empty gaps between min and max row
        c = cols[0]
        for r in range(min(rows), max(rows) + 1):
            pos = r * 15 + c + 1
            if not is_tile(board, pos):
                print("Gap in column placement")
                return False
        return True

    print("Tiles not in a straight line")
    return False


# ---------------------------------------------------------
#  MAIN VALIDATION FUNCTION
# ---------------------------------------------------------

def valid(board, original_board):

    # First move must cover center
    if board[113] in (0, 1):
        return False

    # Find tiles placed this turn
    new_tiles = [pos for pos in range(1, 226)
                 if original_board[pos] == 0 and is_tile(board, pos)]

    # New tiles must be in a straight line with no gaps
    if not in_straight_line(new_tiles, board):
        return False

    # All tiles on the board must form one connected body
    if not all_connected(board):
        return False

    found_words = []

    # -------------------------
    #  Horizontal words
    # -------------------------
    row = 0
    while row < 15:
        temp = ""
        col = 0
        while col < 15:
            idx = row * 15 + col + 1
            if isinstance(board[idx], str) and board[idx].isalpha() or board[idx] == '?':
                temp += board[idx]
            else:
                if len(temp) > 1:
                    found_words.append(temp)
                temp = ""
            col += 1
        if len(temp) > 1:
            found_words.append(temp)
        row += 1

    # -------------------------
    #  Vertical words
    # -------------------------
    col = 0
    while col < 15:
        temp = ""
        row = 0
        while row < 15:
            idx = row * 15 + col + 1
            if isinstance(board[idx], str) and board[idx].isalpha() or board[idx] == '?':
                temp += board[idx]
            else:
                if len(temp) > 1:
                    found_words.append(temp)
                temp = ""
            row += 1
        if len(temp) > 1:
            found_words.append(temp)
        col += 1

    # No words found
    if not found_words:
        return False

    # -------------------------
    #  Validate each word
    # -------------------------
    for w in found_words:
        if not word_matches_with_blanks(w, words):
            print("Invalid:", w)
            return False

    print("Valid:", found_words)
    return True