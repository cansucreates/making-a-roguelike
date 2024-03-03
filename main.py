#!usr/bin/env python3
import tcod

# from actions import EscapeAction, MovementAction
from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from procgen import generate_dungeon

def main() -> None:
    # defining screen size
    screen_width = 80
    screen_height = 50

    # defining map size
    map_width = 80
    map_height = 45
    
    # defining room size
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    
    # defining player position in the middle of the screen
    # int() is used to make sure the position is an integer
    # player_x = int(screen_width / 2) # no need for this anymore
    # player_y = int(screen_height / 2) # no need for this anymore

    # telling tcod to use the font file dejavu10x10_gs_tc.png
    tileset = tcod.tileset.load_tilesheet("dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    # creating a new instance of EventHandler
    event_handler = EventHandler()

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    entities = {npc, player}

    # game_map = GameMap(map_width, map_height)
    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player,
    )

    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    # creating a new terminal with the screen size and the tileset
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Roguelike? more like RogueNotAlike!",
        vsync=True,
    ) as context :
        # creating a new console to draw with the screen size
        # order="F" is for the fortran order [y, x] instead of the c order [x, y]
        root_console = tcod.Console(screen_width, screen_height, order="F") 

        # main game loop
        while True:
            # drawing the console
            # root_console.print(x=player.x, y=player.y, string=player.char, fg=player.color)
            engine.render(console=root_console, context=context)
            # updates the screen with what we have told it to display
            # context.present(root_console)
            events = tcod.event.wait()

            engine.handle_events(events)

            #No need for this anymore after Engine class was created
            """ # clearing the console
            root_console.clear()

            # waiting for the user to close the window
            for event in tcod.event.wait():
                # calling the event_handler's dispatch method with the event
                action = event_handler.dispatch(event)
                # if the action is None, we continue to the next event
                if action is None:
                    continue
                # if the action is an instance of MovementAction, we update the player's position  
                if isinstance(action, MovementAction):
                    player.move(dx=action.dx, dy=action.dy)
                # if the action is an instance of EscapeAction, we raise SystemExit
                elif isinstance(action, EscapeAction):
                    raise SystemExit()    
  """


if __name__ == "__main__":
    main()    