from Engine import GameEngine
from Engine import sendToNode

gameEngine = GameEngine(6,6)
gameEngine.setupPlayers()
sendToNode("READY")
gameEngine.play()
