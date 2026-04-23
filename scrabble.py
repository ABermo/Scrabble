import py5
import random

tile_bag = [
    *('A' * 9),
    *('B' * 2),
    *('C' * 2),
    *('D' * 4),
    *('E' * 12),
    *('F' * 2),
    *('G' * 3),
    *('H' * 2),
    *('I' * 9),
    *('J' * 1),
    *('K' * 1),
    *('L' * 4),
    *('M' * 2),
    *('N' * 6),
    *('O' * 8),
    *('P' * 2),
    *('Q' * 1),
    *('R' * 6),
    *('S' * 4),
    *('T' * 6),
    *('U' * 4),
    *('V' * 2),
    *('W' * 2),
    *('X' * 1),
    *('Y' * 2),
    *('Z' * 1),
    '', ''  # blanks (this will add nothing—see below)
]

def gen_tiles(set, tiles):
    while len(set) < 7:
        index = random.randint(0, len(tiles)-1)
        set.append(tiles[index])
        tiles.pop(index)
    
    set.sort()