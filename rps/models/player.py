
from rps.models.moves import moves
from rps.exceptions import ConflictError


class Player(object):
    def __init__(self, name):
        self.name = name
        self.move = None

    def set_move(self, move):
        if self.move:
            raise ConflictError

        _move = move.lower()

        if not any(map(lambda m: m == _move, moves)):
            raise ValueError

        self.move = move

    def repr_json(self):
        return dict(name=self.name, move=self.move)
