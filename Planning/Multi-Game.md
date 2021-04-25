A Multi-game acts similar to a non multi game except at the end the server first sends a leadboard message in the following format: 

{ "type": "Leadboard",
  "scores": (player-score-list)
}

And sends a replay message to the first client that connected in the following format 

{"type": "replay"}

The Client then prompts the user to ask if they want to continuously until the user inputs True or False. If False the client and server exits. If True the client disconnects and the server waits for players to reconnect to play a new game.