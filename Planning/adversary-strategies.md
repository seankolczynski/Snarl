Adversaries:

All adversaries follow the Adversary Abstract class. All adversaries also follow a 
common architecture, as such: The adversary takes in its surroundings 
on each update, and identifies targets of interest in its FOV. These interests
vary among different adversaries. If there are no targets, or the targets seem
unreachable (i.e. any attempted move towards target is invalid), the Adversary
moves on to a default set of moves (in this case, a random cardinal direction). 
Finally, if the case is such that no move is valid, the Adversary will simply stay put.

Zombies:

Zombies are pretty basic. If a player is within sight range, the zombie will move towards it. 
Otherwise, the zombie will move in a random cardinal direction, unless that direction is a door or is occupied by an adversary

Ghosts:

Ghosts will also go towards the closet player in sight. If no player is around, the ghost then would go towards the nearest wall in sight.
If neither of those are in sight, the ghost simply moves randomly.
