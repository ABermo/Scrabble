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
#  MAIN VALIDATION FUNCTION
# ---------------------------------------------------------

def valid(board):

    # First move must cover center
    if board[113] in (0, 1):
        return False

    # No isolated letters
    if single_letter(board) == False:
        print('Free standing Letter')
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


# ---------------------------------------------------------
#  CHECK FOR ISOLATED LETTERS
# ---------------------------------------------------------

def single_letter(board):
    box = 1
    while box < 226:
        if board[box] not in (0, 1):

            row = (box - 1) // 15
            col = (box - 1) % 15
            touching = False

            if row > 0:
                if board[box - 15] not in (0, 1):
                    touching = True
            if row < 14:
                if board[box + 15] not in (0, 1):
                    touching = True
            if col > 0:
                if board[box - 1] not in (0, 1):
                    touching = True
            if col < 14:
                if board[box + 1] not in (0, 1):
                    touching = True

            if touching == False:
                return False

        box += 1

    return True
