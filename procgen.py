from __future__ import annotations

import random
from typing import Iterator, Tuple, List, TYPE_CHECKING

import tcod

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entity import Entity



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
    
    # This function will be used to check if the rooms intersect
    def intersects(self, other: RectangularRoom) -> bool:
        # Return True if this room overlaps with another RectangularRoom
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

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
    

# # This function will be used to generate the dungeon (NOT NEEDED ANYMORE)
# def generate_dungeon(map_width, map_height) -> GameMap:
#     dungeon = GameMap(map_width, map_height)

#     room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
#     room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

#     dungeon.tiles[room_1.inner] = tile_types.floor
#     dungeon.tiles[room_2.inner] = tile_types.floor

#     # draw the tunnel between the rooms
#     for x, y in tunnel_between(room_2.center, room_1.center):
#         dungeon.tiles[x, y] = tile_types.floor

#     return dungeon    
        
def generate_dungeon(
        max_rooms: int, # maximum number of rooms
        room_min_size: int, # minimum size of the rooms
        room_max_size: int, # maximum size of the rooms
        map_width: int, # width of the map
        map_height: int, # height of the map
        player: Entity, # the player entity
) -> GameMap: 
    """Generate a new dungeon map"""
    dungeon = GameMap(map_width, map_height)

    # list of rooms
    rooms: List[RectangularRoom] = []

    # Generate the rooms
    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue # This room intersects, so go to the next attempt
        # If there are no intersections then the room is valid

        # Dig out this rooms inner area
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room, where the player starts
            player.x, player.y = new_room.center
        else: # All rooms after the first:
            # Dig out a tunnel between this room and the previous one
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor


        # Finally, append the new room to the list
        rooms.append(new_room)

    return dungeon                    

