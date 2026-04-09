import py5

TRIP_WORDS = [1,8,15,106,120,211,218,225]
DOUB_WORDS = [17,29,33,43,49,57,65,71,113,155,161,169,177,183,193,197,209]
TRIP_LETTERS = [21,25,77,81,85,89,137,141,145,149,201,205]
DOUB_LETTERS = [4,12,37,39,46,53,60,93,97,99,103,109,117,123,127,129,133,166,173,180,187,189,214,222]

def setup():
    py5.size(1200,1200)

def draw():
    py5.background('#000000')
    box = 1
    x = 10
    y = 10
    
    while (box < 226):
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
        py5.square(x,y,50)
        
        if box%15 == 0:
            x = 10
            y += 60
        else:
            x += 60
        
        box += 1
    
py5.run_sketch()