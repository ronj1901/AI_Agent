# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
import random

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.__agentCoordinate = [(0,0,"Right")]
        self.__safeTiles = [[0,0]]
        
        #movement flags
        self.left = False
        self.forward = False
        self.right = False
        self.wentAdj = False
        
        self.gameStart = True
        self.wumpusKilled = False
        self.arrow = True
        self.goHome = False
        self.currLoc = (0,0)
        self.stenchList = set()
        self.breezeList = set()
        self.safeList = set()
        self.possiblePitList = set()
        self.possibleWumpusList = set()
        self.PitList = set()
        self.wumpusLoc = ()
        self.currDir = "RIGHT"
        self.boundaryLoc = [10,10]
        self.goldLooted   = False
        
        self.__actions = [
            Agent.Action.TURN_LEFT,
            Agent.Action.TURN_RIGHT,
            Agent.Action.FORWARD,
            Agent.Action.CLIMB,
            Agent.Action.SHOOT,
            Agent.Action.GRAB
        ]
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        



        if self.gameStart == True:
            if breeze:
                return Agent.Action.CLIMB

        if stench and self.arrow:
            self.stenchList.add(self.currLoc)
            self.arrow = False
            return Agent.Action.SHOOT

        if scream:
            self.wumpusKilled = True
            self.possibleWumpusList.clear()
            self.stenchList.clear()
        elif self.arrow == False:
            if self.currDir == ("RIGHT"):
                self.wumpusLoc = (self.currLoc[0], self.currLoc[1] + 1)
            if self.currDir == ("UP"):
                self.wumpusLoc = (self.currLoc[0] + 1, self.currLoc[1])

        if self.goldLooted == True:
            #backtrack
            pass
        
        self.gameStart = False

        x, y = self.currLoc[0], self.currLoc[1]

        if bump:
            if self.currDir == "RIGHT":
                self.currLoc = (x - 1, y)
                self.boundaryLoc[0] = x - 1
                adjacentBox = self.findAdjacentTiles(x-1,y)
            if self.currDir == "UP":
                self.currLoc = (x, y - 1)
                self.boundaryLoc[1] = y - 1
                adjacentBox = self.findAdjacentTiles(x,y-1)
            x, y = self.currLoc[0], self.currLoc[1]

        
        self.safeList.add((x,y))
        adjacentBox = self.findAdjacentTiles(x,y)


        if stench and not self.wumpusKilled:
            self.stenchList.add((x,y))
            for i in adjacentBox:
                if i not in self.safeList:
                    self.possibleWumpusList.add(i)

        if breeze:
            self.breezeList.add((x,y))
            for i in adjacentBox:
                if i not in self.safeList:
                    self.possiblePitList.add(i)

        print (" \nFor Debugging Purposes:")
        print ("Current Location: " + str(self.currLoc) + " Current Direction: " + self.currDir)
        print ("Stench List: " + str(self.stenchList) + " Breeze List: " + str(self.breezeList))
        print ("Possible Wumpus List: " + str(self.possibleWumpusList) + "Possible Pit List: " + str(self.possiblePitList))
        print ("GameStart: " + str(self.gameStart))
        print ("Boundary Location: " + str(self.boundaryLoc))
        print ("Possible Move List: " + str(adjacentBox) + " Safe List:" + str(self.safeList))
        print ("Stench List: " + str(self.stenchList) + " Breeze List: " + str(self.breezeList))


        if self.left == True:
            self.left = False
            return self.move(self.currDir, self.currLoc, "LEFT")
        
        if self.forward == True:
            self.forward = False
            return self.move(self.currDir, self.currLoc, self.currDir)

        if glitter:
            self.goldLooted = True
            self.goHome = True
            #backtrack
            return Agent.Action.GRAB

        return self.bestMove(adjacentBox, self.currDir, self.currLoc, self.possiblePitList, self.possibleWumpusList, stench, breeze, scream, self.arrow)
        
        '''if glitter:
            self.goldLooted = True
            return Agent.Action.GRAB 
        
        if stench:
            #self.safeTile.append(currLoc)
            self.stenchList.append(self.currLoc)
            return self.move("BACK", self.currLoc, self.currDir)
        if breeze:  
            #self.safeTile.append(currLoc)
            self.breezeList.append(self.currLoc)
            return self.move("BACK", self.currLoc, self.currDir)
        
        if bump:
            if self.currDir == "RIGHT" or self.currDir == "LEFT":
                self.boundaryLoc[0] = self.currLoc[0]
                return self.move("LEFT", self.currLoc, self.currDir)
            elif self.currDir == "UP" or self.currDir == "DOWN":
                self.boundaryLoc[1] = self.currLoc[1]
                return self.move("RIGHT", self.currLoc, self.currDir)
            
        return self.move("FORWARD", self.currLoc, self.currDir)''' 
        
        #return Agent.Action.CLIMB
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================


    def findAdjacentTiles(self, x, y):
        li =[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]

        #x = [i for i in li if i[0]%self.boundaryLoc[0] == self.boundaryLoc[0] or i[1]%self.boundaryLoc[1] == self.boundaryLoc[1] or i[0] == -1 or i[1] == -1]
        x = [i for i in li if (i[0] > self.boundaryLoc[0]) or (i[1] > self.boundaryLoc[1]) or (i[0] == -1) or (i[1] == -1)]
    
        return {i for i in li if i not in x}

    '''def updateDir(self, direct, cDirect):
        if direct == "LEFT":
            if cDirect == "RIGHT":
                self.currDir = "UP"
            elif cDirect == "UP":
                self.currDir = "LEFT"
            elif cDirect == "LEFT":
                self.currDir = "DOWN"
            elif cDirect == "DOWN":
                self.currDir = "RIGHT"
        if direct == "RIGHT":
            if cDirect == "RIGHT":
                self.currDir = "DOWN"
            elif cDirect == "UP":
                self.currDir = "RIGHT"
            elif cDirect == "LEFT":
                self.currDir = "UP"
            elif cDirect == "DOWN":
                self.currDir = "DOWN"
    
    def updateLoc(self, coord, cDirect):
        if cDirect == "UP":
            self.currLoc[1] += 1
        elif cDirect == "DOWN":
            self.currLoc[1] -= 1 
        elif cDirect == "RIGHT":
            self.currLoc[0] += 1 
        elif cDirect == "LEFT":
            self.currLoc[0] -= 1'''
                
    def bestMove(self, pMove, cDir, cLoc, pPit, pWumpus, stn, brz, scrm, arr):

        '''
            
        '''

        pMove = {i for i in pMove if i not in (self.PitList.union({self.wumpusLoc}))}

        up = False
        down = False
        left = False
        right = False

        for i in pMove:
            if (i[0] - cLoc[0]) == 1:
                right = True
                print ("Right is True")
            if (i[0] - cLoc[0]) == -1:
                left = True
                print ("Left is True")
            if (i[1] - cLoc[1]) == 1:
                up = True
                print ("Up is True")
            if (i[1] - cLoc[1]) == -1:
                down = True
                print ("Down is True")

        if self.goHome == True:
            if cLoc == (0,0):
                return Agent.Action.CLIMB

            if (cDir == "LEFT" or cDir == "RIGHT") and left == True:
                return self.move(cDir, cLoc, "LEFT")
            else:
                return self.move(cDir, cLoc, "DOWN")
            if (cDir == "UP" or cDir == "DOWN") and down == True:
                return self.move(cDir, cLoc, "DOWN")
            else:
                return self.move(cDir, cLoc, "LEFT")


        if self.wentAdj == True:
            if cDir == "LEFT":
                return self.move(cDir, cLoc, "UP")
            if cDir == "DOWN":
                return self.move(cDir, cLoc, "RIGHT")

        if stn and scrm == True:
            return self.move(cDir, cLoc, cDir)

        if brz:
            self.wentAdj = True
            return self.goAdj(cLoc, cDir)

        if cDir == "UP" and up == True:
            return self.move(cDir, cLoc, cDir)
        if cDir == "DOWN" and down == True:
            return self.move(cDir, cLoc, cDir)
        if cDir == "LEFT" and left == True:
            return self.move(cDir, cLoc, cDir)
        if cDir == "RIGHT" and right == True:
            return self.move(cDir, cLoc, cDir)


    def goAdj(self, cLoc, cDir):
        if cDir == "UP":
            return self.move(cDir,cLoc,"DOWN")
        if cDir == "DOWN":
            return self.move(cDir,cLoc,"UP")
        if cDir == "LEFT":
            return self.move(cDir,cLoc,"RIGHT")
        if cDir == "RIGHT":
            return self.move(cDir,cLoc,"LEFT")

    def cost(self, cDir, fDir):

        if cDir == "RIGHT":
            if fDir == "UP":
                return 2
            if fDir == "RIGHT":
                return 1
            if fDir == "LEFT":
                return 3
            if fDir == "DOWN":
                return 2

        if cDir == "UP":
            if fDir == "LEFT":
                return 2
            if fDir == "UP":
                return 1
            if fDir == "DOWN":
                return 3
            if fDir == "RIGHT":
                return 2

        if cDir == "LEFT":
            if fDir == "DOWN":
                return 2
            if fDir == "LEFT":
                return 1
            if fDir == "RIGHT":
                return 3 
            if fDir == "UP":
                return 2

        if cDir == "DOWN":
            if fDir == "RIGHT":
                return 2
            if fDir == "DOWN":
                return 1
            if fDir == "UP":
                return 3
            if fDir == "LEFT":
                return 2

    def move(self, cDir, cLoc, fDir):

        if cDir == "RIGHT":
            if fDir == "UP":
                self.currDir = "UP"
                self.forward = True
                return Agent.Action.TURN_LEFT
            if fDir == "RIGHT":
                self.currLoc = (self.currLoc[0] + 1, self.currLoc[1])
                return Agent.Action.FORWARD
            if fDir == "LEFT":
                self.currDir = "UP"
                self.left = True
                return Agent.Action.TURN_LEFT 
            if fDir == "DOWN":
                self.currDir = "DOWN"
                self.forward = True
                return Agent.Action.TURN_RIGHT

        if cDir == "UP":
            if fDir == "LEFT":
                self.currDir = "LEFT"
                self.forward = True
                return Agent.Action.TURN_LEFT
            if fDir == "UP":
                self.currLoc = (self.currLoc[0], self.currLoc[1] + 1)
                return Agent.Action.FORWARD
            if fDir == "DOWN":
                self.currDir = "LEFT"
                self.left = True
                return Agent.Action.TURN_LEFT 
            if fDir == "RIGHT":
                self.currDir = "RIGHT"
                self.forward = True
                return Agent.Action.TURN_RIGHT

        if cDir == "LEFT":
            if fDir == "DOWN":
                self.currDir = "DOWN"
                self.forward = True
                return Agent.Action.TURN_LEFT
            if fDir == "LEFT":
                self.currLoc = (self.currLoc[0] - 1, self.currLoc[1])
                return Agent.Action.FORWARD
            if fDir == "RIGHT":
                self.currDir = "DOWN"
                self.left = True
                return Agent.Action.TURN_LEFT 
            if fDir == "UP":
                self.currDir = "UP"
                self.forward = True
                return Agent.Action.TURN_RIGHT

        if cDir == "DOWN":
            if fDir == "RIGHT":
                self.currDir = "RIGHT"
                self.forward = True
                return Agent.Action.TURN_LEFT
            if fDir == "DOWN":
                self.currLoc = (self.currLoc[0], self.currLoc[1] - 1)
                return Agent.Action.FORWARD
            if fDir == "UP":
                self.currDir = "RIGHT"
                self.left = True
                return Agent.Action.TURN_LEFT 
            if fDir == "LEFT":
                self.currDir = "LEFT"
                self.forward = True
                return Agent.Action.TURN_RIGHT

        
        '''if direct == "BACK":
            self.left = True
            self.updateDir("LEFT", cDirect)
            return Agent.Action.TURN_LEFT 
        elif direct == "RIGHT":
            self.forward = True 
            return Agent.Action.TURN_RIGHT 
        elif direct == "LEFT":
            self.forward = True 
            self.updateDir(direct, cDirect)
            return Agent.Action.TURN_LEFT 
        elif direct == "FORWARD":
            self.updateLoc(coord, cDirect) 
            return Agent.Action.FORWARD'''
            
    
            
    def  filterThreatList(self, threatList, safelist):
        return [i for i in threatList if i not in safelist]
    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
