
import uuid

from rps.models.game import Game
from rps.exceptions import NotFoundError


class GameService(object):
    games = dict()

    def new_game(self, name):
        game_id = str(uuid.uuid4())

        new_game = Game()
        new_game.add_player(name)

        self.games[game_id] = new_game

        return game_id

    def join_game(self, gameId, name):
        game = self.get_game(gameId)

        if(game is None):
            raise NotFoundError

        game.add_player(name)

    def make_move(self, game_id, name, move):
        game = self.get_game(game_id)

        if(game is None):
            raise NotFoundError

        game.make_move(name, move)

    def get_game(self, gameId):
        return self.games.get(gameId, None)
