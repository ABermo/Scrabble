data = open('dictionary.txt', 'r')
words = data.read()
words = words.split('\n')

def valid(board):
    if board[113] in (0,1):
        return False
    
    
    
    if single_letter(board) == False:
        print('Free standing Letter')
        return False

    found_words = []

    row = 0
    while row < 15:
        temp = ""
        col = 0
        while col < 15:
            idx = row * 15 + col + 1
            if isinstance(board[idx], str) and board[idx].isalpha():
                temp += board[idx]
            else:
                if len(temp) > 1:
                    found_words.append(temp)
                temp = ""
            col += 1
        if len(temp) > 1:
            found_words.append(temp)
        row += 1

    col = 0
    while col < 15:
        temp = ""
        row = 0
        while row < 15:
            idx = row * 15 + col + 1
            if isinstance(board[idx], str) and board[idx].isalpha():
                temp += board[idx]
            else:
                if len(temp) > 1:
                    found_words.append(temp)
                temp = ""
            row += 1
        if len(temp) > 1:
            found_words.append(temp)
        col += 1

    if not found_words:
        return False

    for w in found_words:
        if w not in words:
            print("Invalid:", w)
            return False

    print("Valid:", found_words)
    return True


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
