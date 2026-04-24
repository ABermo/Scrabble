import py5
import random

"""
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
    '?', '?'  # blanks (this will add nothing—see below)
]
"""

tile_bag = [
    *('A' * 13),
    *('H' * 10),
    *('I' * 10),
    *('N' * 7),
    *('R' * 7),
    *('E' * 6),
    *('S' * 6),

    *('C' * 4),
    *('D' * 4),
    *('L' * 4),
    *('O' * 4),
    *('T' * 4),
    *('G' * 3),
    *('U' * 3),

    *('Á' * 2),
    *('F' * 2),
    *('Í' * 2),
    *('M' * 2),

    *('É' * 1),
    *('Ó' * 1),
    *('Ú' * 1),

    *('B' * 1),
    *('P' * 1),

    '?', '?'   # 2 blank tiles
]


def gen_tiles(set, tiles):
    while len(set) < 7:
        index = random.randint(0, len(tiles)-1)
        set.append(tiles[index])
        tiles.pop(index)
    
    set.sort()