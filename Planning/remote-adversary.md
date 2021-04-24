Remote Adversaries:
Our remote adversaries are controlled via human input, as a player movement would be.
This was relatively simple to add, as we had been planning for it from the very first time the idea was mentioned by Dio.
The client class simply received a new variable that indicates whether the  client is controlling a player or a 
monster, and the view is printed appropriately for each. Other than that, handling of moves is the same, as the RuleChecker
was already being applied to all movements made on the game. The ease of this transfer was largely due to planning ahead, 
as we made all Characters be controlled by a "Driver" class, whether it be a human driver or an AI one. That way, no matter 
who is driving, the game treat them the same. There are no issues of backwards compatibility, as choosing the type of character is 
the only change, and the original form of game can still be played. No extensions had to be made to protocol, as both receive the same updates. The only difference
is the layout received, as monsters receive the full view.