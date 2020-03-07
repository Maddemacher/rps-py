from flask import jsonify, request
import json

from rps import app
from rps.services.gameService import GameService
from rps.utils.json import ComplexEncoder
from rps.exceptions import NotFoundError, GameFullError, ConflictError

game_service = GameService()


@app.route("/api/games")
def all_games():
    return json.dumps(game_service.games, cls=ComplexEncoder)


@app.route('/api/game', methods=['POST'])
def new_games():
    if(not request.json['name']):
        return "", 400

    game_id = game_service.new_game(
        request.json['name']
    )

    return game_id, 201, {'location': '/api/game/%s' % game_id}


@app.route('/api/game/<string:game_id>/join', methods=['PUT'])
def join_game(game_id):
    try:
        game_service.join_game(
            game_id,
            request.json['name']
        )
    except NotFoundError:
        return "", 404
    except GameFullError:
        return "", 412
    except ConflictError:
        return "", 409

    return "OK"


@app.route('/api/game/<string:game_id>/move', methods=['PUT'])
def make_move(game_id):
    try:
        game_service.make_move(
            game_id,
            request.json['name'],
            request.json['move']
        )
    except NotFoundError:
        return "", 404
    except ValueError:
        return "", 400
    except ConflictError:
        return "", 409

    return "OK"


@app.route('/api/game/<string:game_id>')
def get_game(game_id):
    game = game_service.get_game(game_id)

    if (game == None):
        return "", 404

    return json.dumps(game, cls=ComplexEncoder)
