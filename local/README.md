To play our version of Snarl, you first have to set the necessary flags to play the game.

Setting the observe flag to 1 will add an observer view to the game, showing a separate window into everything that's happening.

You can set the player from 1 to 4 players to get that many players to play. Giving more the game will throw an error or giving less than 1 will throw an error

Setting the levels flag will take you to a custom path to the levels you have on file. If the levels file is not valid it will also throw an error.

Setting the start flag will put you and other players on the level specified, this is one indexed.


How to play:

For each player you will be given a view with

p - representing a player
g - representing a ghost
z - representing a zombie
K - representing a key
E - representing an exit

Under your view you will be given your current position. To move your character on your turn you will type in the coordinates as

x(space)y

Where X is the column you want to be in and Y is the row you want to be in. Hitting enter will make your move be nothing. If you put in an invalid move you will be prompted for a move again. Each new level you will be randomly places somewhere on the level. If you happen to have taken all the keys off the level and go to the exit when there's a Zombie or Ghost on it, you will die on the next level. The logic behind this is while the exit is open you pass through it and the adversary. It kills you but your body will go to the next level. When the game is over your stats will be presented. After you input your move, any event that occurred will display under your input, you may need to scroll up to see it.
