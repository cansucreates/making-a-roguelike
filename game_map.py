import numpy as np # type: ignore
from tcod.console import Console

import tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        # create a 2D array of tiles
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")
        # set the first 3 columns in the middle of the map to be walls
        self.tiles[30:33, 22] = tile_types.wall

    # check if a pair of coordinates is within the bounds of the map
    def in_bounds(self, x:int, y:int) -> bool:
        # Return True if x and y are inside the bounds of this map
        return 0 <= x < self.width and 0 <= y < self.height
    #  render the map
    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]