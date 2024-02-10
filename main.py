#!usr/bin/env python3
import tcod

def main() -> None:
    # defining screen size
    screen_width = 80
    screen_height = 50
    
    # defining player position in the middle of the screen
    # int() is used to make sure the position is an integer
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # telling tcod to use the font file dejavu10x10_gs_tc.png
    tileset = tcod.tileset.load_tilesheet("dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

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
            root_console.print(x=player_x, y=player_y, string="@")
            # updates the screen with what we have told it to display
            context.present(root_console)

            # waiting for the user to close the window
            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()


if __name__ == "__main__":
    main()    