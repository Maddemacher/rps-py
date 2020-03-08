

import enum


class Move(enum.Enum):
    rock = 0
    paper = 1
    scissors = 2

    def repr_json(self):
        return self.name

    def __eq__(self, other):
        return self.value == other

    def __gt__(self, other):
        if self.value > other.value:
            return True

        return other == Move.scissors and self.value == Move.rock
