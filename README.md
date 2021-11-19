# CA314-Snake-and-Ladders

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