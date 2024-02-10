class Action:
    pass

# will be when we hit the Esc key (subclass of Action)
class EscapeAction(Action):
    pass

# will be used to describe our player moving around (subclass of Action)
class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy
