
import uuid

from rps.models.game import Game
from rps.exceptions import NotFoundError


class GameService:
    games = dict()

    def new_game(self, name: str) -> str:
        game_id = str(uuid.uuid4())

        new_game = Game()
        new_game.add_player(name)

        self.games[game_id] = new_game

        return game_id

    def join_game(self, game_id: str, name: str):
        game = self.get_game(game_id)

        if game is None:
            raise NotFoundError

        game.add_player(name)

    def make_move(self, game_id: str, name: str, move: str):
        game = self.get_game(game_id)

        if game is None:
            raise NotFoundError

        game.make_move(name, move)

    def get_game(self, game_id: str) -> Game:
        return self.games.get(game_id, None)
