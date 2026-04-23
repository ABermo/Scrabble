import py5
import scrabble
import validation

#special tile co-ordinates
TRIP_WORDS = [1,8,15,106,120,211,218,225]
DOUB_WORDS = [17,29,33,43,49,57,65,71,113,155,161,169,177,183,193,197,209]
TRIP_LETTERS = [21,25,77,81,85,89,137,141,145,149,201,205]
DOUB_LETTERS = [4,12,37,39,46,53,60,93,97,99,103,109,117,123,127,129,133,166,173,180,187,189,214,222]

#player racks
player1 = []
player2 = []
inuse = []
temp_rack = []

#coordiante n = current_position[n]
current_position = [0] * 226

def setup():
    global temp_rack
    py5.size(1500,1500)
    py5.text_size(60)
    py5.background('#000000')
    
    scrabble.gen_tiles(player1, scrabble.tile_bag)
    temp_rack = player1.copy()

def draw():
    board()
    show_tiles(player1)
    click()
    letter_enter(player1)
    show_board()
    
   
def board():
    box = 1
    x = 10
    y = 10
    
    #drawing boxes
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
        
        if current_position[box] == 1:
            py5.no_fill()
            py5.stroke("#d7b015")
            py5.stroke_weight(5)
            py5.rect(x + 2.5, y + 2.5, 45, 45)
            py5.no_stroke()
            
        if box%15 == 0:
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
        py5.square(x,y,50)
        
        py5.fill('#FFFFFF')
        py5.text(box, x + 5, y + 45)
        
        x += 60
     
# highlight the selected cell   
def click():
    if py5.is_mouse_pressed:
        x = py5.mouse_x
        y = py5.mouse_y
        
        col = (x//60) + 1
        row = (y//60)
        
        pos = row * 15 + col
        
        if 1 in current_position:
            current_position[current_position.index(1)] = 0
        
        current_position[pos] = 1
            
def letter_enter(tiles):
    if py5.is_key_pressed:
        key = py5.key.upper()
        
        if key in tiles:
            if 1 in current_position and key in temp_rack:
                current_position[current_position.index(1)] = key
                inuse.append(key)
                temp_rack.pop(temp_rack.index(key))
        
        if py5.key in ("RETURN", "\n"):
            validation.valid(current_position)
        
        
    
    key = ''

def show_board():
    box = 1
    x = 10
    y = 10
    
    while (box < 226):
        if (current_position[box] != 0) and (current_position[box] != 1):
            py5.fill('#FFFFFF')
            py5.text(current_position[box], x + 5, y + 45)
        
        if box%15 == 0:
            x = 10
            y += 60
        else:
            x += 60
            
        box += 1

py5.run_sketch()