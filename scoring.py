# --- Bonus tile coordinates ---
TRIP_WORDS = [1,8,15,106,120,211,218,225]
DOUB_WORDS = [17,29,33,43,49,57,65,71,113,155,161,169,177,183,193,197,209]
TRIP_LETTERS = [21,25,77,81,85,89,137,141,145,149,201,205]
DOUB_LETTERS = [4,12,37,39,46,53,60,93,97,99,103,109,117,123,127,129,133,166,173,180,187,189,214,222]

# --- Tile values ---
tile_values = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2,
    'E': 1, 'F': 4, 'G': 2, 'H': 4,
    'I': 1, 'J': 8, 'K': 5, 'L': 1,
    'M': 3, 'N': 1, 'O': 1, 'P': 3,
    'Q': 10,'R': 1, 'S': 1, 'T': 1,
    'U': 1, 'V': 4, 'W': 4, 'X': 8,
    'Y': 4, 'Z': 10,
    '?': 0
}

# --- Find all words on the board ---
def find_words(board):
    words = []

    # horizontal
    for r in range(15):
        temp = ""
        pos_list = []
        for c in range(15):
            pos = r * 15 + c + 1
            if board[pos] not in (0, 1):
                temp += board[pos]
                pos_list.append(pos)
            else:
                if len(temp) > 1:
                    words.append((temp, pos_list.copy()))
                temp = ""
                pos_list = []
        if len(temp) > 1:
            words.append((temp, pos_list.copy()))

    # vertical
    for c in range(15):
        temp = ""
        pos_list = []
        for r in range(15):
            pos = r * 15 + c + 1
            if board[pos] not in (0, 1):
                temp += board[pos]
                pos_list.append(pos)
            else:
                if len(temp) > 1:
                    words.append((temp, pos_list.copy()))
                temp = ""
                pos_list = []
        if len(temp) > 1:
            words.append((temp, pos_list.copy()))

    return words


# --- Score the move ---
def score_move(original_board, current_board):
    total_score = 0

    # tiles placed this turn
    new_tiles = [i for i in range(1, 226)
                 if original_board[i] == 0 and current_board[i] not in (0, 1)]

    if not new_tiles:
        return 0

    words = find_words(current_board)

    # only score words containing at least one new tile
    scorable_words = [
        (word, positions)
        for word, positions in words
        if any(pos in new_tiles for pos in positions)
    ]

    for word, positions in scorable_words:
        word_score = 0
        word_multiplier = 1

        for pos in positions:
            letter = current_board[pos]
            letter_score = tile_values[letter]

            # blanks never get multipliers
            if letter != '?':
                if pos in new_tiles:
                    if pos in TRIP_LETTERS:
                        letter_score *= 3
                    elif pos in DOUB_LETTERS:
                        letter_score *= 2

                if pos in new_tiles:
                    if pos in TRIP_WORDS:
                        word_multiplier *= 3
                    elif pos in DOUB_WORDS:
                        word_multiplier *= 2

            word_score += letter_score

        total_score += word_score * word_multiplier

    return total_score
