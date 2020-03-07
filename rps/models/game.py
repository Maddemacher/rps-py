
from dataclasses import asdict

from rps.models.player import Player
from rps.models.moves import Move
from rps.exceptions import GameFullError, ConflictError, NotFoundError


class Game:
    def __init__(self):
        self.players = []
        self.status = None
        self.result = None

    def _evaluate_winner(self):
        if self.players[0].move == self.players[1].move:
            self.result = 'tie'
            return

        if self.players[0].move > self.players[1].move:
            self.result = f'{self.players[0].name} wins'
            return

        self.result = f'{self.players[1].name} wins'

    def _evaluate(self):
        if len(self.players) < 2:
            self.status = "Ongoing"
            return

        if any(map(lambda p: p.move is None, self.players)):
            self.status = "waiting for moves"
            return

        self.status = "done"
        self._evaluate_winner()

    def _get_player(self, name: str) -> Player:
        player = next(p for p in self.players if p.name == name)

        if player is None:
            raise NotFoundError

        return player

    def make_move(self, name: str, move: Move):
        player = self._get_player(name)

        player.set_move(move)

        self._evaluate()

    def add_player(self, name: str):
        if len(self.players) == 2:
            raise GameFullError

        if any(map(lambda p: p.name == name, self.players)):
            raise ConflictError

        self.players.append(Player(name))

    def repr_json(self) -> dict:
        if self.status == 'done':
            return dict(
                players=list(map(lambda p: asdict(p), self.players)),
                status=self.status,
                result=self.result
            )

        return dict(
            players=list(map(lambda p: dict(name=p.name), self.players)),
            status=self.status,
            result=self.result,
        )
