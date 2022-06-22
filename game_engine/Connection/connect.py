import time
import random
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Connect():
    def __init__(self, player, queue, publisher):
        self.player = player
        self.queue = queue
        self.publisher = publisher

    def wait_connection(self):
        count = 0
        while self.publisher.get_subscription_count() != 1:
            clear()
            print('Waiting on other player' + ('.'*((count+1) % 3)))
            time.sleep(1)
            count += 1 
        self.publisher.send('READY')
        msg = self.queue.read(wait=True)
        if msg:
            if msg == 'READY':
                clear()
                print('CONNECTED')
                return True

    def roll_a_dice(self):
        playerNumber = 0
        targetPlayerNumber = 0
        while playerNumber == targetPlayerNumber:
            playerNumber = random.randint(0,100)
            self.publisher.send(str(playerNumber))
            targetPlayerNumber = int(self.queue.read(wait=True))
            print('You rolled a ' + str(playerNumber) + ' and the other player an ' + str(targetPlayerNumber))
            if playerNumber > targetPlayerNumber:
                print('You begin :)')
                return True
            elif playerNumber < targetPlayerNumber:
                print('The other player begins :(')
                return False
            else:
                print('It\'s a tie, rolling again..')
            



