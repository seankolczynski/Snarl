  Part 1: Overall, we plan to use a model-view-controller setup, where all players
will share the model, a controller (probably a web server) that takes in and
handles actions, and the view, which will  present the game in different forms to
different players. The only internal state we are holding is the player ID. This
ID will help the game identify which player corresponds to which user. A player
object  will represent every player in the  model, and its actions will be modified
by the Snarl controller, which will get actions from the client program. The
client program also handles the view on the players end, as each view has to be
unique.
	Every Character in the game will share a Character Interface. This entity will
have an HP, a movement speed, and two arrays: An array of attack moves, and an inventory.
This will be in the interface for the time being, until we decide whether or not
we want monsters to have inventory space. Players each have unique names and IDs,
and all other parts are part of  an abstract class. Players have two methods,
move() and attack(). Inventory objects will be kept as a string. For now, attacks
are a dictionary of name and damage value, but this is subject to change  based
on upcoming design requirements
	Adversaries extend a Character and have three methods. AImove(), which makes a
move based on built in logic, AIplace() which behaves similarly, and AIAttack(),
in case the game is advanced beyond the original spec.
	Maps are represented in the object gameModel, in a 2D-array of tiles. A tile
can be either normal, walled, or exit tile. With a normal tile being able to hold
a character, an item, or nothing, and a walled tile being able to not hold anything
or have a player on it, an exit tile corresponding to a specific key. When
players move, they must query this map to ensure that there is no wall there or
they can move to the exit.
	When a player moves, the client will send a move command to the server. The
server will validate the move, and if valid, it will move the player and return
their new position.

Part 2: Milestones

1. First, we must make the model, enemy, player structures.
2. Next, we want to be able to fully generate a level, with players and adversaries.
3. Player movement, attacks, and pickups.
4. Game is fully playable and bug tested on the server end.
5. Client wirings and communication enabled, along with controller.
6. Client is able to draw the state of the game nicely.
7. Player can initialize a multiplayer game, and players can join that game.
8. Game startup and shutdown is clean
9. Fully playable, final version
