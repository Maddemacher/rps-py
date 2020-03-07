
import json


def _get_game(client, game_id, expected_status=200):
    response = client.get(f'/api/game/{game_id}')

    assert response.status_code == expected_status

    if (expected_status == 200):
        return json.loads(response.get_data(as_text=True))

    return None


def _create_game(client, name='emil', expected_status=201):
    response = client.post(
        '/api/game',
        data=json.dumps({'name': name}),
        content_type='application/json'
    )

    assert response.status_code == expected_status

    if expected_status == 201:
        return response.get_data(as_text=True)

    return None


def _join_player(client, game_id, name='lasse', expected_status=200):
    response = client.put(
        f'/api/game/{game_id}/join',
        data=json.dumps({'name': name}),
        content_type='application/json'
    )

    assert response.status_code == expected_status


def _make_move(client, game_id, name, move, expected_status=200):
    response = client.put(
        f'/api/game/{game_id}/move',
        data=json.dumps({
            'name': name,
            'move': move,
        }),
        content_type='application/json'
    )

    assert response.status_code == expected_status


def test_get_unknown_game(client):
    _get_game(client, "asd", 404)


def test_create_new_game(client):
    game_id = _create_game(client)
    game = _get_game(client, game_id)

    assert len(game['players']) == 1
    assert game['players'][0]['name'] == "emil"

    return game_id


def test_create_new_game_without_name(client):
    game_id = _create_game(client, "", 400)
    game_id = _create_game(client, None, 400)


def test_join_second_player(client):
    game_id = _create_game(client)
    _join_player(client, game_id)

    game = _get_game(client, game_id)

    assert len(game['players']) == 2
    assert game['players'][1]['name'] == "lasse"


def test_cant_join_third_player(client):
    game_id = _create_game(client)
    _join_player(client, game_id)
    _join_player(client, game_id, "hej", 412)

    game = _get_game(client, game_id)

    assert len(game['players']) == 2
    assert game['players'][1]['name'] == "lasse"


def test_join_player_with_same_name(client):
    game_id = _create_game(client, "emil")
    _join_player(client, game_id, "emil", 409)

    game = _get_game(client, game_id)

    assert len(game['players']) == 1


def test_make_moves(client):
    game_id = _create_game(client, "emil")
    _join_player(client, game_id, "lasse")

    _make_move(client, game_id, "emil", "rock")
    _make_move(client, game_id, "lasse", "rock")

    game = _get_game(client, game_id)


def test_make_unknown_move(client):
    game_id = _create_game(client, "emil")

    _make_move(client, game_id, "emil", "asd", 400)


def test_does_not_show_moves_until_done(client):
    game_id = _create_game(client, "emil")

    _make_move(client, game_id, "emil", "rock")
    game = _get_game(client, game_id)

    assert game['players'][0]['name'] == 'emil'
    assert not 'move' in game['players'][0]


def test_player_one_wins(client):
    game_id = _create_game(client, "emil")
    _join_player(client, game_id, "lasse")

    _make_move(client, game_id, "emil", "paper")
    _make_move(client, game_id, "lasse", "rock")

    game = _get_game(client, game_id)

    assert game['result'] == 'emil wins'


def test_player_two_wins(client):
    game_id = _create_game(client, "emil")
    _join_player(client, game_id, "lasse")

    _make_move(client, game_id, "emil", "paper")
    _make_move(client, game_id, "lasse", "scissors")

    game = _get_game(client, game_id)

    assert game['result'] == 'lasse wins'


def test_tie(client):
    game_id = _create_game(client, "emil")
    _join_player(client, game_id, "lasse")

    _make_move(client, game_id, "emil", "paper")
    _make_move(client, game_id, "lasse", "paper")

    game = _get_game(client, game_id)

    assert game['result'] == 'tie'


def test_rock_beats_scissors(client):
    game_id = _create_game(client, "emil")
    _join_player(client, game_id, "lasse")

    _make_move(client, game_id, "emil", "rock")
    _make_move(client, game_id, "lasse", "scissors")

    game = _get_game(client, game_id)

    assert game['result'] == 'emil wins'


def test_scissors_beat_paper(client):
    game_id = _create_game(client, "emil")
    _join_player(client, game_id, "lasse")

    _make_move(client, game_id, "emil", "scissors")
    _make_move(client, game_id, "lasse", "paper")

    game = _get_game(client, game_id)

    assert game['result'] == 'emil wins'


def test_paper_beats_rock(client):
    game_id = _create_game(client, "emil")
    _join_player(client, game_id, "lasse")

    _make_move(client, game_id, "emil", "paper")
    _make_move(client, game_id, "lasse", "rock")

    game = _get_game(client, game_id)

    assert game['result'] == 'emil wins'
