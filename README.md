# CA314-Snake-and-Ladders

## Requirements
The version of python need to be equal or upper than 3.9

The project development was make with the python version (3.9.9)

Install this requires packages : 
```
pip install pygame
pip install load_dotenv
```

After that, create .env file :

Take the data inside the .env.example for creating your .env

Else, you have just to rename the .env.example file into .env

## Run the program

-> Linux

You can use the files server_game.sh and snakes_and_ladders.sh which are bash scripts that launch respectively the server and 4 clients (required).

-> Windows

You can use the files server_game.bat and lunch_4_clients.bat which are batch scripts that launch the server and the 4 clients respectively (required).

-> Through a terminal on any OS

Lunch the server :
```
cd server
python Game.py
```

Lunch a client:  
```
cd client
python Game.py
```

## Events (Receive):

### Server:
-> ME: when the server accpet the client connection
REMOVE_PLAYER: remove player from queue ()
ADD_PLAYER: add player to match queue and and his username. Define his color (username) -> LIST_PLAYERS
-> GAME_START: if 4 players

-> PLAYER_TURN 
ROLL_DICE: roll the dice () -> PLAYER_ROLLING_DICE
-> PLAYER_DICE
-> UPDATE_PLAYERS list of players, if a player quit the game

-> GAME_END remove all players data (username, color)


### Client:
ME: uid player (uid)
-> ADD_PLAYER 
LIST_PLAYERS: players in the match queue (players: [username, uid, color])
-> REMOVE_PLAYER if the player quit the queue
GAME_START: start the game (snakes: [(start, end)], ladders: [(start, end)], order: [uid])

UPDATE_PLAYERS: players in the game (players: [username, uid, color])
PLAYER_TURN: player turn (uid)
-> ROLL_DICE
PLAYER_ROLLING_DICE : start animation ()
PLAYER_DICE: dice value (uid, value, position)

GAME_END: define winner (uid)

-> ADD_PLAYER: in order to play again 