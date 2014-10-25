import sys
import re
from sudokuUtil import *
import numpy as np
varC = ['A','B','C','D','E','F','G','H','I']

class CSP:

	def __init__(self,filename):
		self.X = []
		self.V = []
		self.C = []
		self.init(filename)

	# Initializing values for variables
	def init(self,filename):
		for i in range(9):
			for j in range(1,10):
				var = varC[i]+str(j)
				self.X.append(var)
				values = set([1,2,3,4,5,6,7,8,9])
				self.V.append(values)
		gamelist = []
		try:
            		for line in open(filename):
                		if(len(line)!=10):
                    			print "Error: file format invalid"
                    			sys.exit(1)
				#print line
				#line=line.replace(" ","").replace("\r","").replace("\n","")
				#line=line.replace("0","*").replace("\r","").replace("\n","")
				#print line
				gamelist = gamelist + list(line.rstrip())
        	except IOError as e:
           		print "Error: file cannot be opened"
            		sys.exit(1)
		for i in range(len(gamelist)):
			if(re.match("\d+",gamelist[i])):
				self.V[i] = set([int(gamelist[i])])
		self.constraints()

	# Setting variables for arc consistency for rows and columns
	def constraints(self):
		for i in self.X:
			for j in self.X:
				if not((i[0] == j[0] and i[1] != j[1]) or (i[1] == j[1] and i[0] != j[0])):
					continue
				else:
					cond = True
					for c in self.C:
						if(i in c and j in c):
							cond = False
					if(cond):
						self.C.append(set([i,j]))
		for i in [0,3,6]:
			for j in [0,3,6]:
				self.cubeConstraints(i,j)

	# Setting variables for arc consistency for cubes
	def cubeConstraints(self,a,b):
		cubeList = []
		for i in range(a,a+3):
			for j in range(b,b+3):
				x = varC[i]+str(j+1)
				cubeList.append(x)
		for i in cubeList:
			for j in cubeList:
				if not(i[0] != j[0] or i[1] != j[1]):
					continue
				else:
					cond = True
					for c in self.C:
						if(i in c and j in c):
							cond = False
					if(cond):
						self.C.append(set([i,j]))
	# Get list of neighbors
	def get_neighbors(self,x):
		index = self.X.index(x)
		row = index / 9
		col = index % 9
		neighbors = []
		for i in range(1,10):
			varRow = varC[row]+str(i)
			varCol = varC[i-1]+str(col+1)
			if(i != col+1):
				neighbors.append(varRow)
			if(i != row+1):
				neighbors.append(varCol)
		a = (row / 3) * 3
		b = (col / 3) * 3
		for i in range(a,a+3):
			for j in range(b,b+3):
				y = varC[i]+str(j+1)
				if(y != x and y not in neighbors):
					neighbors.append(y)
		return neighbors

	# Check if assignment has completed assigned all values
	def is_complete(self,assignment):
		index = 0
		for v in self.V:
			if(len(v)>1 and self.X[index] not in assignment):
				return False
			index += 1
		return True

	# Check if selected value is consistent with the assignment
	def is_consistent(self,x,v):
		neighbors = self.get_neighbors(x)
		for n in neighbors:
			v = self.V[self.X.index(n)]
			if(len(v) == 1 and x in v):
				consistent = False
		return True 

	# Display the sudoku game 
#	def print_game(self):
#		count = 0
#		#arr=[]
		#arr.append(self.V)
##		#print arr[0]
#		nl = "\n"
#		np= " "
#		with open("solution.txt", "a") as myfile:
#			myfile.seek(0)
#    			myfile.truncate()
#			myfile.close()				
##		for v in self.V:
#			st = str(v.pop())
#			sys.stdout.write(st)	
#			with open("solution.txt", "a") as myfile:
#    				myfile.write(st)
#			
#			count += 1
##			if count%9 != 0:
#				with open("solution.txt", "a") as myfile:
#                                        myfile.write(np)
#			if count%9 == 0 and count<81:
#				with open("solution.txt", "a") as myfile:
#					myfile.write(nl)
##			#arr.append(v)
#			#print arr
			#save_sudoku('solution.txt',v)
##			if((count % 9)== 0):
				#print arr
#				#save_sudoku('solution.txt',arr)
#				#del arr[:]
#				print ""

	def print_game(self):
		 count = 0
		 for d in self.V:
			 sys.stdout.write(str(d.pop()))
			 count += 1
			 if((count % 9)== 0):
			 	print ""
	# Check if all variables values have been assigned.
	def is_solved(self):
		solved = True
		for v in self.V:
			if(len(v)>1):
				solved = False
		return solved

	# Set the assigned values to variables
	def assign(self,assignment):
		for x in assignment:
			self.V[self.X.index(x)] = set([assignment[x]])
