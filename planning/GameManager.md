Class GameManager:
	// levels is a list of Floors
           // gameState is a GameState
           // playerRulechecker is a RuleChecker subclass for players
	Def init(self, levels):
	     Self.gameState = GameState(levels)
                 self.playerRuleChecker = PlayerRulechecker()
	     Self.players = {}
              Player -> void 
	// adds a player to GameManager
           // returns an error if the name is not unique
	add_player(self, player):

	// We decided that the GameState can return the view for a specific player. This method will get the player’s location and view distance, and return the grid they can “see” from the GameState’s current floor

	player_view(self, player):
		