  # -*- coding: latin-1 -*-
import random
import sys
sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import addCoords
from AIPlayerUtils import *


##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    ##
    def __init__(self, inputPlayerId):
        #Called it a temp name for now
        super(AIPlayer,self).__init__(inputPlayerId, "Drone_AI")
        #Variables to store coordinates of the agent's food, tunnel, and anthill
        # self.myFoodForTunnel = None
        # self.myFoodForAnthill = None
        self.myTunnel = None
        self.myAnthill = None
    
    ##
    #getPlacement
    #
    #Description: The getPlacement method corresponds to the 
    #action taken on setup phase 1 and setup phase 2 of the game. 
    #In setup phase 1, the AI player will be passed a copy of the 
    #state as currentState which contains the board, accessed via 
    #currentState.board. The player will then return a list of 11 tuple 
    #coordinates (from their side of the board) that represent Locations 
    #to place the anthill and 9 grass pieces. In setup phase 2, the player 
    #will again be passed the state and needs to return a list of 2 tuple
    #coordinates (on their opponent's side of the board) which represent
    #Locations to place the food sources. This is all that is necessary to 
    #complete the setup phases.
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is
    #       requesting a placement from the player.(GameState)
    #
    #Return: If setup phase 1: list of eleven 2-tuples of ints -> [(x1,y1), (x2,y2),…,(x10,y10)]
    #       If setup phase 2: list of two 2-tuples of ints -> [(x1,y1), (x2,y2)]
    ##
    def getPlacement(self, currentState):
        self.myFoodForTunnel = None
        self.myFoodForAnthill = None
        self.myTunnel = None
        self.myAnthill = None

        if(self.playerId == PLAYER_ONE):
            enemy = PLAYER_TWO
        else:
            enemy = PLAYER_ONE

        # Variable to hold opponent's inventory
        enemyInventory = currentState.inventories[enemy]
        # Variables to hold opponent's anthill and tunnel coordinates
        enemyAnthillCoords = enemyInventory.constrs[0].coords
        enemyTunnelCoords = enemyInventory.constrs[1].coords

        print "enemy team: ", enemy
        print "my team: ", self.playerId
        print "    enemy tunnel coords", enemyTunnelCoords
        print "    enemy anthill coords", enemyAnthillCoords

        if currentState.phase == SETUP_PHASE_1:
            # Indexes 0-1: Anthill, tunnel
            # Indexes 2-10: Grass
            return [(0,0), (8, 2),
                    (0,2), (1,2), (2,1), (7,3), \
                    (0,3), (1,1), (8,3), \
                    (0,1), (9,3) ];
        elif currentState.phase == SETUP_PHASE_2:
            numToPlace = 2
            foodLocations = []

            for i in range(0, numToPlace):
                LargestDistanceIndex = [(-1,-1)]
                LargestDistance = 0
                foodLocation = None
                while foodLocation == None:
                    for i in range(BOARD_LENGTH):
                        for j in range(6,10):
                            if currentState.board[i][j].constr == None and (i, j) not in foodLocations:
                                currentDistance = approxDist((i,j),(enemyTunnelCoords)) + approxDist((i,j),(enemyAnthillCoords))
                                if  currentDistance > LargestDistance:
                                    print "  index: ", i,j
                                    print "    dist from tunnel: ", currentDistance
                                    LargestDistance = currentDistance
                                    LargestDistanceIndex = (i,j)
                    print "Food location picked"
                    foodLocation = LargestDistanceIndex
                foodLocations.append(foodLocation)
            return foodLocations
        else:
            return None
    
    ##
    #getMove
    #Description: The getMove method corresponds to the play phase of the game 
    #and requests from the player a Move object. All types are symbolic 
    #constants which can be referred to in Constants.py. The move object has a 
    #field for type (moveType) as well as field for relevant coordinate 
    #information (coordList). If for instance the player wishes to move an ant, 
    #they simply return a Move object where the type field is the MOVE_ANT constant 
    #and the coordList contains a listing of valid locations starting with an Ant 
    #and containing only unoccupied spaces thereafter. A build is similar to a move 
    #except the type is set as BUILD, a buildType is given, and a single coordinate 
    #is in the list representing the build location. For an end turn, no coordinates 
    #are necessary, just set the type as END and return.
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is 
    #       requesting a move from the player.(GameState)   
    #
    #Return: Move(moveType [int], coordList [list of 2-tuples of ints], buildType [int]
    ##
    def getMove(self, currentState):
        # Useful pointers
        myInv = getCurrPlayerInventory(currentState)
        me = currentState.whoseTurn

        # Variable to hold total number of worker ants
        numOfWorkerAnts = len(getAntList(currentState, me, (WORKER,)))

        # List of all ally worker ants
        myWorkers = getAntList(currentState, me, (WORKER,))

        #anthillCoords = myInv.getAnthill().coords

        # the first time this method is called, the food and tunnel locations
        # need to be recorded in their respective instance variables
        if self.myTunnel == None:
            self.myTunnel = getConstrList(currentState, me, (TUNNEL,))[0]
        if self.myAnthill == None:
            self.myAnthill = getConstrList(currentState, me, (ANTHILL,))[0]
        #if self.myFoodForTunnel == None or self.myFoodForAnthill == None:
            # foods = getConstrList(currentState, None, (FOOD,))
            # self.myFoodForTunnel = foods[0]
            # self.myFoodForAnthill = foods[1]
            # # find the food closest to the tunnel
            # bestDistToTunnel = 1000  # i.e., infinity
            # bestDistToAnthill = 1000
            # for food in foods:
            #     distToAnthill = stepsToReach(currentState, self.myAnthill.coords, food.coords)
            #     distToTunnel = stepsToReach(currentState, self.myTunnel.coords, food.coords)
            #
            #     if distToAnthill < bestDistToAnthill:
            #         self.myFoodForAnthill = food
            #         bestDistToAnthill = distToAnthill
            #     if distToTunnel < bestDistToTunnel:
            #         self.myFoodForTunnel = food
            #         bestDistToTunnel = distToTunnel


        # If all the workers have moved, we're done
        lastWorker = getAntList(currentState, me, (WORKER,))[numOfWorkerAnts - 1]
        if (lastWorker.hasMoved):
            return Move(END, None, None)

        # if the queen is on the anthill move her
        if myInv.getQueen().coords == myInv.getAnthill().coords:
            return Move(MOVE_ANT, [myInv.getQueen().coords, (1, 0)], None)

        # Creates enough workers to have 2 on the board (if we have food and anthill empty)
        if myInv.foodCount > 0 and numOfWorkerAnts < 2:
            if (getAntAt(currentState, myInv.getAnthill().coords) is None):
                return Move(BUILD, [myInv.getAnthill().coords], WORKER)
        # Creates drones if we already have enough workers
        # elif (myInv.foodCount > 2):
        #     if (getAntAt(currentState, myInv.getAnthill().coords) is None):
        #         return Move(BUILD, [myInv.getAnthill().coords], DRONE)

        # Move all my drones towards the enemy
        myDrones = getAntList(currentState, me, (DRONE,))
        for drone in myDrones:
            if not drone.hasMoved:
                droneX = drone.coords[0]
                droneY = drone.coords[1]
                if droneY < 9:
                    droneY += 1;
                else:
                    droneX += 1;
                if (droneX, droneY) in listReachableAdjacent(currentState, drone.coords, 3):
                    return Move(MOVE_ANT, [drone.coords, (droneX, droneY)], None)
                else:
                    return Move(MOVE_ANT, [drone.coords], None)

        allMoves = listAllMovementMoves(currentState)

        for worker in myWorkers:
            if not worker.hasMoved:
                if worker.carrying:
                    # See if ant closer to anthill or tunnel, move to closest

                    if (stepsToReach(currentState,worker.coords,self.myAnthill.coords)
                            < (stepsToReach(currentState,worker.coords,self.myTunnel.coords))):
                        path = createPathToward(currentState, worker.coords,
                                                self.myAnthill.coords, UNIT_STATS[WORKER][MOVEMENT])
                    else:
                        path = createPathToward(currentState, worker.coords,
                                                self.myTunnel.coords, UNIT_STATS[WORKER][MOVEMENT])

                    return Move(MOVE_ANT, path, None)
                else:
                    foods = getConstrList(currentState, None, (FOOD,))
                    bestDist = 1000
                    myFood = None
                    for food in foods:
                        distToAnthill = stepsToReach(currentState, self.myAnthill.coords, food.coords)
                        distToTunnel = stepsToReach(currentState, self.myTunnel.coords, food.coords)

                        if distToAnthill < distToTunnel:
                            if distToAnthill < bestDist:
                                myFood = food
                                bestDist = distToAnthill
                        else:
                            if distToTunnel < bestDist:
                                myFood = food
                                bestDist = distToTunnel

                    path = createPathToward(currentState, worker.coords,
                                            myFood.coords, UNIT_STATS[WORKER][MOVEMENT])
                    return Move(MOVE_ANT, path, None)

        # # if the worker has food, move toward tunnel
        # if (myWorker.carrying):
        #     path = createPathToward(currentState, myWorker.coords,
        #                             self.myTunnel.coords, UNIT_STATS[WORKER][MOVEMENT])
        #     return Move(MOVE_ANT, path, None)
        #
        # # if the worker has no food, move toward food
        # else:
        #     path = createPathToward(currentState, myWorker.coords,
        #                             self.myFood.coords, UNIT_STATS[WORKER][MOVEMENT])
        #     return Move(MOVE_ANT, path, None)

        return None
    
    ##
    #getAttack
    #Description: The getAttack method is called on the player whenever an ant completes 
    #a move and has a valid attack. It is assumed that an attack will always be made 
    #because there is no strategic advantage from withholding an attack. The AIPlayer 
    #is passed a copy of the state which again contains the board and also a clone of 
    #the attacking ant. The player is also passed a list of coordinate tuples which 
    #represent valid locations for attack. Hint: a random AI can simply return one of 
    #these coordinates for a valid attack. 
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is requesting 
    #       a move from the player. (GameState)
    #   attackingAnt - A clone of the ant currently making the attack. (Ant)
    #   enemyLocation - A list of coordinate locations for valid attacks (i.e. 
    #       enemies within range) ([list of 2-tuples of ints])
    #
    #Return: A coordinate that matches one of the entries of enemyLocations. ((int,int))
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        return enemyLocations[0]  # don't care
        
    ##
    #registerWin
    #Description: The last method, registerWin, is called when the game ends and simply 
    #indicates to the AI whether it has won or lost the game. This is to help with 
    #learning algorithms to develop more successful strategies.
    #
    #Parameters:
    #   hasWon - True if the player has won the game, False if the player lost. (Boolean)
    #
    def registerWin(self, hasWon):
        #method template, not implemented
        pass
