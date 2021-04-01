  Server                      Client             Player
  |                           |                   |
  | <-------------------------| startGame()       |
  |                           |                   |
  | createGame()              |                   |
  | generateMap()             |                   |
  | sendView() -------------->|                   |
                              | draw() ---------> |
  |<--------------------------| makeMove() <----  | Move
  |                           |                   |
  | validateMove()----------> |                   |
  | sendView() -------------->| draw() ---------> |
  | updateGame()--+           |                   |
  |               |           |                   | 
  |               |           |                   | 
  |  <------------+           |                   | 
  | sendView() -------------->| draw() ---------> |
------  Repeat  ----------------------------
  | endGame() --------------->|
