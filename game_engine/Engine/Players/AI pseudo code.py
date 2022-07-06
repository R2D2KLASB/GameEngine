movesDone = empty list                                              //list to store done moves
moves, AImoves = lists with all coordinates                         //Create 2 lists with all coordinates
startCoordinate = NULL                                              //Save the first hit on a ship
currentCoordinate = NULL                                            //Save the last shot on a ship
lastShot = random                                                   //Save the last type of shot

function Turn():
    if random:                                                      //The AI wants to do a random shot
        coordinate = AImoves[random_int]                            //Get an random coordinate from the smart coordinate list
    if XLeft:                                                       //The AI does a shot horizontal left
        coordinate = currentCoordinate X-1
    if XRight:                                                      //The AI does a shot horizontal right
        coordinate = currentCoordinate X+1
    if YLower:                                                      //The AI does a shot vertical under
        coordinate = currentCoordinate Y+1
    if YHigher:                                                     //The AI does a shot vertical above
        coordinate = currentCoordinate Y-1
    if coordinate in moves:
        Shoot the other player at coordinate                        //Hit the player on the coordinate
        movesDone.append(coordinate)                                //Add the coordinate to the done list
        RemoveMoves()                                               //Optimise the AI

        The result of the shot is:
        hit:
            if lastShot == random:
                lastShot = a random direction                       //The next shot should be somewhere around the hit
            if shipKilled:
                remove all coordinates around ship from lists       //The rules say you cant place ships next to each other
                lastShot = random                                   //the ship is gone, it can go back to trying to find new ships

        miss:
            if lastShot is NOT random:                              //If the AI found a ship but a shot is miss
                go to the next position around the hit

        invalid:
            return Turn()                                           //Try again to get a valid coordinate
        else:                                                       //Shot was valid
            remove the coordinate from moves and AIMoves
    else:
        return Turn()                                               //Try again to get a valid coordinate

function RemoveMoves():                                             //The AI can save time/shots by placing them smart
    for move in movesDone:
        if there is a coordinate in AImoves closer dan SMALLESTSHIP from move:
            remove this coordinate from AImoves

function PlaceShips():
    for ship in ships:                                              //loop trough the possible ships
        if the coordinate in not forbidden:                         //The rules tell ships can't be placed next to each other
            give the ship a random coordinate, and random direction