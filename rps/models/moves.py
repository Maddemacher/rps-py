

import enum


class Move(enum.Enum):
    Rock = 0
    Paper = 1
    Scissors = 2

    @classmethod
    def from_string(cls, value):
        if value == "rock":
            return cls.Rock

        if value == "paper":
            return cls.Paper

        if value == "scissors":
            return cls.Scissors

        raise ValueError

    def repr_json(self):
        return self.name

    def __eq__(self, other):
        return self.value == other

    def __gt__(self, other):
        if self.value > other.value:
            return True

        return other == Move.Scissors and self.value == Move.Rock
