# responsible for drawing the map and the entities on the screen, and handling the players input

from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

# from actions import EscapeAction, MovementAction
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            # we are not using this anymore, since we are using the perform method from the Action class
            # if isinstance(action, MovementAction):
            #     # if the tile we are trying to move to is walkable, we move the player
            #     if self.game_map.tiles["walkable"][self.player.x + action.dx, self.player.y + action.dy]:
            #        self.player.move(dx=action.dx, dy=action.dy)

            # elif isinstance(action, EscapeAction):
            #     raise SystemExit()

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()                