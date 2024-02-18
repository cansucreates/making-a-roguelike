import random
from typing import Iterator, Tuple

import tcod

from game_map import GameMap
import tile_types



# This class will be used to create the rooms in the game
class RectangularRoom:
    # takes x and y coordinates, width and height
    def __init__(self, x:int, y:int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    # describes the cx and y of the center of the room
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        # Return the inner area of this room as a 2D array index
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)  


# This function will be used to create the tunnel between the rooms
# all the tuples are used to represent the coordinates of the rooms    
def tunnel_between(
        start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points"""
    # unpack the coordinates
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5: # 50% chance
        # move horizontally, then vertically
        corner_x, corner_y = x2, y1
    else: 
        # move vertically, then horizontally
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel
    # using the bresenham algorithm to draw the lines
    # yield is used to return a generator      
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y                
    

# This function will be used to generate the dungeon    
def generate_dungeon(map_width, map_height) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
    room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

    dungeon.tiles[room_1.inner] = tile_types.floor
    dungeon.tiles[room_2.inner] = tile_types.floor

    # draw the tunnel between the rooms
    for x, y in tunnel_between(room_2.center, room_1.center):
        dungeon.tiles[x, y] = tile_types.floor

    return dungeon    