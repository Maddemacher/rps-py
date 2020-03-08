from flask import jsonify, request, abort
import json

from rps import app
from rps.models.moves import Move
from rps.services.gameService import GameService
from rps.utils.json import ComplexEncoder
from rps.exceptions import NotFoundError, GameFullError, ConflictError

game_service = GameService()


@app.route("/api/games")
def all_games():
    return json.dumps(game_service.games, cls=ComplexEncoder)


@app.route('/api/game', methods=['POST'])
def new_games():
    if not request.json['name']:
        abort(400)

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
        abort(404)
    except GameFullError:
        abort(412)
    except ConflictError:
        abort(409)

    return "OK"


@app.route('/api/game/<string:game_id>/move', methods=['PUT'])
def make_move(game_id):
    try:
        move = request.json['move']

        if move is None:
            abort(400)

        game_service.make_move(
            game_id,
            request.json['name'],
            Move[move.lower()]
        )
    except NotFoundError:
        abort(404)
    except KeyError:
        abort(400)
    except ConflictError:
        abort(409)

    return "OK"


@app.route('/api/game/<string:game_id>')
def get_game(game_id):
    game = game_service.get_game(game_id)

    if game is None:
        abort(404)

    return json.dumps(game, cls=ComplexEncoder)
