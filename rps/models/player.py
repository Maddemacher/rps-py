
from dataclasses import dataclass, asdict


from rps.models.moves import Move
from rps.exceptions import ConflictError


@dataclass
class Player:
    name: str
    move: Move = None

    def set_move(self, move: Move):
        if self.move:
            raise ConflictError

        self.move = move
