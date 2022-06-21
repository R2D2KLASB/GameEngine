from .Engine import GameEngine


def main(args=None):
    gameEngine = GameEngine(6,6)
    gameEngine.setupPlayers()
    gameEngine.play()


if __name__ == '__main__':
    main()