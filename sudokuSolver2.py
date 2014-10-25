import os
import sys
import copy
import time
from Queue import PriorityQueue
from Queue import Queue
from sudokuUtil import *

class SudokuSolver():
    
    def __init__(self):
        self.puzzle=[] #Initialize the puzzle
        self.blanks=[] #Initialize blank spots
        self.initPuzzleArray() #Construct an array of 0 0 0 0 0...
        
        self.blankValues={} #Initialize the dictionary for heuristic
                       
        self.pathLengths=[] #Hold all the path lengths for metrics
        self.currentPathLength=0 #Hold the local path length
        self.constraintChecks=0 
        self.runningTime=0
        
        self.start()
        
    def start(self):
	self.puzzle = load_sudoku('puzzle.txt')

        self.blanks=self.getEmptyCells(self.puzzle)
        
	self.processVariablesFH()   
	retValue=self.constraintProp()
        if(retValue==None):
            self.forwardCheckHeuristic()
        

    def backTrack(self, index):
        if index>len(self.blanks)-1:
            self.endAlgorithm()
        
        row=self.blanks[index][0]
        col=self.blanks[index][1]
        
        for num in range(1, 10):
            if self.puzzleValid(row, col, num, False):   
                self.currentPathLength+=1 
                self.puzzle[row][col] = num
                self.backTrack(index+1)
        
        self.pathLengths.append(self.currentPathLength) #Add the current path length to the overall list.
        self.currentPathLength-=1 #-1 from path.
        index-=1
        self.puzzle[row][col]=0

    def backTrackHeuristic(self):
        if len(self.blanks)==0:
            self.endAlgorithm()    
            
        nextBlank=self.getMRV()#Get the most constrained blank
        
        row=nextBlank[0]
        col=nextBlank[1]

        for num in range(1, 10):
            if self.puzzleValid(row, col, num, False):
                self.blanks.remove(nextBlank)
                self.currentPathLength+=1
                self.puzzle[row][col] = num
                result=self.backTrackHeuristic()
                if result!=None:    
                   return
            
                self.currentPathLength-=1
                self.pathLengths.append(self.currentPathLength)
                self.blanks.append(nextBlank)
                self.puzzle[row][col]=0 
                
        return None
    
    def forwardCheck(self, index):
        if index>len(self.blanks)-1:
            self.endAlgorithm()
        
        blank=self.blanks[index]
        row=blank[0]
        col=blank[1]
        
        blankDomain=copy.deepcopy(self.blankValues[blank])
        
        for num in blankDomain:            
            tempDomain=copy.deepcopy(self.blankValues) #Copy of current domain before pruning
            consistent=self.pruneInvalid(blank, num)
            if (consistent==True): #Assign a value and recurse if domain processing returned true
                self.puzzle[row][col] = num
                self.currentPathLength+=1
                
                result=self.forwardCheck(index+1)
                if result!=None:
                    return
            
            self.blankValues=tempDomain #Fell through; restore the domain
                
        self.puzzle[row][col]=0
        self.pathLengths.append(self.currentPathLength) #Add the current path length to the overall list.
        self.currentPathLength-=1 #-1 from path.
        index-=1
        return None
    
    def forwardCheckHeuristic(self):
        if len(self.blanks)==0:
            self.endAlgorithm()
        
        blank=self.getMRV()
        row=blank[0]
        col=blank[1]

        blankDomain=copy.deepcopy(self.blankValues[blank])

        for num in blankDomain:
            tempDomain=copy.deepcopy(self.blankValues) #Copy of current domain before pruning
            consistent=self.pruneInvalid(blank, num)
            if (consistent==True): #Assign a value and recurse if domain processing returned true
                self.blanks.remove(blank)
                self.puzzle[row][col] = num
                self.currentPathLength+=1
                
                result=self.forwardCheckHeuristic()
                if result!=None:
                    return  
                
                self.blankValues=tempDomain #Restore the original domain
                
                self.blanks.append(blank)
                self.puzzle[row][col]=0
                self.pathLengths.append(self.currentPathLength) #Add the current path length to the overall list.
                self.currentPathLength-=1
        return None
    
    def constraintProp(self):
        if len(self.blanks)==0:
            self.endAlgorithm()
        
        blank=self.getMRV()
        row=blank[0]
        col=blank[1]

        blankDomain=copy.deepcopy(self.blankValues[blank])

        for num in blankDomain:
            tempDomain=copy.deepcopy(self.blankValues) #Copy of current domain before pruning
            self.blankValues[blank]=[num]
            self.propagateConstraints()
            self.puzzle[row][col]=num
            
            self.currentPathLength+=1
            self.blanks.remove(blank)   
            
            result=self.constraintProp()
            if result!=None:
                return
            self.blankValues=tempDomain
            self.blanks.append(blank)
            self.puzzle[row][col]=0
            self.pathLengths.append(self.currentPathLength) #Add the current path length to the overall list.
            self.currentPathLength-=1
        return None

    def puzzleValid(self, row, col ,num, heur):
        if heur==False:
            self.constraintChecks+=1 #Increment number of constraint checks
        valid=False
        if num==0:
            return True
        else:
            rowValid=self.checkRow(row, num)
            colValid=self.checkColumn(col, num)
            boxValid=self.checkBox(row, col, num)                                   
            valid=(rowValid&colValid&boxValid)
    
        return valid

    def checkRow(self, row, num):
        for col in range(9):
	    currentValue=self.puzzle[row][col]
            if num==currentValue:
                return False        
        return True
    
    def checkColumn(self, col, num ):
        for row in range(9):
            currentValue=self.puzzle[row][col]
            if num==currentValue:
                return False
        return True

    def checkBox(self, row, col, num):       
        row=(row/3)*3
        col=(col/3)*3
        
        for r in range(3):
            for c in range(3):
                if self.puzzle[row+r][col+c]==num:
                    return False
        return True
    

    def getMRV(self):
        
        q = PriorityQueue()
        for blank in self.blanks:
            possible = self.getPossibleValues(blank, True)
	    q.put((len(possible), blank))
        blanks = []
        blanks.append(q.get())
        minVal = blanks[0][0]

        while not q.empty(): #Get all equally-prioritized blanks
            next = q.get()
            if next[0] == minVal:
                blanks.append(next)
            else:
                break
            
        maxDeg = len(self.getNeighborBlanks(blanks[0][1]))
        maxDegBlank = blanks[0]

        for blank in blanks:
            degree = len(self.getNeighborBlanks(blank[1]))
            if degree > maxDeg:
                maxDegBlank = blank
                maxDeg = degree
        return maxDegBlank[1]
    def processVariablesF(self):        
        for blank in self.blanks:
            possibleValues=self.getPossibleValues(blank, False)
            self.blankValues[blank]=possibleValues
    
    def processVariablesFH(self):
        for blank in self.blanks:
            possibleValues=self.getPossibleValues(blank, False)
            self.blankValues[blank]=possibleValues

    def pruneInvalid(self, blank, num):
        neighbors=self.getNeighborBlanks(blank)
        for neighborBlank in neighbors:
            neighborDomain=self.blankValues[neighborBlank]
            if num in neighborDomain:
                self.blankValues[neighborBlank].remove(num)
                if len(self.blankValues[neighborBlank])==0: #Detect empty domain
                    return False
        return True
    def propagateConstraints(self):
        queue=Queue() #Build a queue of all arcs in the grid
        for blank in self.blanks:
            neighbors=self.getNeighborBlanks(blank)
            for neighbor in neighbors:
                queue.put((blank, neighbor))

        while not queue.empty():
            arc=queue.get()
            orig=arc[0]
            dest=arc[1]
            if self.removeInconsistencies(orig, dest): #Removal occurred from orig
                neighbors=self.getNeighborBlanks(orig) #Go through neighbors, add an arc from neighbor->orig to detect possible inconsistencies
                neighbors.remove(dest)
                for neighbor in neighbors:
                    queue.put((neighbor, orig))

    def removeInconsistencies(self, orig, dest):
        removed=False
        originDomain=copy.deepcopy(self.blankValues[orig])
        for val in originDomain:
            neighborDomain=copy.deepcopy(self.blankValues[dest])
            if val in neighborDomain: 
                neighborDomain.remove(val)                
            if len(neighborDomain)==0: #Any value of original domain caused neighbor domain to become 0
                self.blankValues[orig].remove(val)
                removed=True
        return removed
    def endAlgorithm(self):
            self.pathLengths.append(self.currentPathLength) #Append the final path's length
            self.runningTime=time.clock()-self.runningTime
	    save_sudoku('solution.txt', self.puzzle)
            self.printMetrics()
            sys.exit(0)
            
    def getPossibleValues(self, cell, heur):
        row=cell[0]
        col=cell[1]
        allowed=[]
        for i in range(1,10):
            if self.puzzleValid(row, col, i, heur):
                allowed.append(i)
    
        return allowed
    
    def getEmptyCells(self, puzzle):
        emptyCells=[]
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j]==0:
                    emptyCells.append((i, j))
        return emptyCells
    
    def getNeighborBlanks(self, blank):
        row=blank[0]
	col=blank[1]

	neighbors=[]
        associatedBlanks=self.getRowBlanks(row)+self.getColumnBlanks(col)+self.getBoxBlanks(row, col)
        for blank in associatedBlanks:
            if blank not in neighbors and blank!=(row,col): 
                neighbors.append(blank)
        return neighbors
        
    def getRowBlanks(self, row):
        cells=[]
        for col in range(9):
            if self.puzzle[row][col]==0:
                cells.append((row, col))
        return cells
    
    def getColumnBlanks(self, col ):
        cells=[]
        for row in range(9):
            if self.puzzle[row][col]==0:    
                cells.append((row,col))
        
        return cells
    
    def getBoxBlanks(self, row, col):       
        cells=[]
        row=(row/3)*3
        col=(col/3)*3
        
        for r in range(3):
            for c in range(3):
                if self.puzzle[row+r][col+c]==0:
                    cells.append((row+r,col+c))
                    
        return cells

    def initPuzzleArray(self):
        del self.puzzle[:]
        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append([])
                self.puzzle[i][j]=0
                
    def printPuzzle(self):
        rowStrings=[]
        for i in range(9):
            rowString=[]
            for j in range(9):
                rowString.append(str(self.puzzle[i][j])+" ")
            rowStrings.append(self.formatRow(rowString))
        for i in range(0, len(rowStrings), 3):
            for j in range(0, 3):
                print rowStrings[i+j]
    
    def printMetrics(self):
        #print "Constraint checks: "+str(self.constraintChecks)
        print "Running time: "+str(self.runningTime)
        #print "Number of paths: "+str(len(self.pathLengths))
        #print "Deepest path: "+str(max(self.pathLengths))
        #print "Average path length: "+str(float(sum(self.pathLengths))/len(self.pathLengths))
        print "Solution Below: "
        self.printPuzzle()
        print ""
        
        
    def formatRow(self, rowString):
        formattedString=""
        for i in range(0, len(rowString), 3):
            for j in range(0, 3):
                formattedString+=rowString[i+j]
            formattedString+=""
            
        return formattedString
    
            
SudokuSolver()
