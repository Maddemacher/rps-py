#! /bin/bash

PORT=3000

GAME=`http POST :$PORT/api/game name=emil`
http PUT :$PORT/api/game/$GAME/join name=lasse
http PUT :$PORT/api/game/$GAME/move name=lasse move=rock
http PUT :$PORT/api/game/$GAME/move name=emil move=paper
http :$PORT/api/game/$GAME

# http :$PORT/api/games
