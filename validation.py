data = open('dictionary.txt', 'r')
words = data.read()
words = words.split('\n')

def valid(board):
    box = 1
    temp = ''
    active = False
    while (box < 226):
        if board[box] != 0 and active == False:
            temp = board[box]
            active = True
        elif board[box] != 0 and active == True:
            temp += board[box]
        if board[box] == 0 and active == True:
            active = False
            
            if len(temp) > 1:
                if temp not in words:
                    print('Invalid')
                    return False
                else:
                    print('Valid')
                    return True
        box += 1