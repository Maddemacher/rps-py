
from dataclasses import dataclass, asdict


from rps.models.moves import moves
from rps.exceptions import ConflictError


@dataclass
class Player:
    name: str
    move: str = None

    def set_move(self, move: str):
        if self.move:
            raise ConflictError

        _move = move.lower()

        if not any(map(lambda m: m == _move, moves)):
            raise ValueError

        self.move = move
