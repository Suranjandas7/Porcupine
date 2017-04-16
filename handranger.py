#Make and Save Poker Hand Ranges
#using numpy and matplotlib

import numpy as np
import matplotlib.pyplot as plt

class range_maker(object):
	def __init__(self, name):
		#loads data from data.dat to numpy 2-d array back_board
		self.range = np.zeros(shape = (13,13), dtype = 'int')
		self.back_board = np.zeros(shape = (13,13), dtype = 'int')
		self.name = name
		f = open('data.dat', 'rb') #data.dat contains hand rankings for each specific hand.
		raw_lines = []
		for line in f.readlines(): raw_lines.append(line[:-2])
		for x in xrange(0,13): self.back_board[x] = raw_lines[x].split('|')
		f.close()

	def translate(self, input): #to convert the input into the plot co-ordinates
		refer = {'A':0,'K':1,'Q':2,'J':3,'T':4,'9':5,'8':6,'7':7,'6':8,'5':9,'4':10,'3':11,'2':12}
		output = refer[input]
		return output

	def Overall_percentile(self, percent): 		#makes a specific range based on inputed percentile and stores it in 2D array self.range
		hand_range_maximus = (float(percent)/100)*169
		self.name = self.name + ' (' + str(percent) + ' %)'
		for x in xrange(0,13): 
			for y in xrange(0,13):
				if self.back_board[x][y] < hand_range_maximus: self.range[x][y] = 1
				else: self.range[x][y] = 0

	def Xx(self, MainString, Limit, OyS): #Xx(0/1) -> mark any range of a particular card (for example 'J', '7', 0 will mark all J off suite cards to J7o)
		Limit = self.translate(Limit)
	 	MainString = self.translate(MainString)
	 	if OyS is 1:
	 		for x in range(MainString,Limit+1):
				self.range[MainString][x] = 1
			for x in range(MainString,Limit-1, -1):
				self.range[x-1][MainString] = 1
	 	elif OyS is 0:
	 		for x in range(int(MainString), Limit):
	 			self.range[x+1][MainString] = 1
	 		for x in range(Limit,int(MainString)):
	 			self.range[MainString][x] = 1
	 	else:
	 		return 'Invalid Input'

	def Pairs(self, StartPair, Limit): #mark pairs from StartPair to Limit
		Limit = self.translate(Limit)
	 	StartPair = self.translate(StartPair)
	 	for x in range(StartPair,Limit+1):
	 		self.range[x][x] = 1

	def show_range(self): #show the range contained in range_maker
		ax = plt.axes()
		ax.set_xticks(np.arange(0,15,1))
		ax.set_yticks(np.arange(0,15,1))
		ax.plot(xrange(0,13), xrange(0,13), '-g', label = 'DIVIDE')

		plt.grid(True, linestyle = "-")
		plt.style.use('seaborn-whitegrid')
		plt.title(self.name)
		plt.imshow(self.range, cmap = 'summer') #summer, blues, autumn_r

		points = []
		for x in xrange(0,13):
			for y in xrange(0,13):
				points.append([x,y])
		x = map(lambda x: x[0], points)
		y = map(lambda x: x[1], points)

		labels = [item.get_text() for item in ax.get_xticklabels()]
		id = {0:'A', 1: 'K', 2: 'Q', 3: 'J', 4: 'T', 5: '9', 6: '8', 7: '7', 8:'6', 9:'5', 10: '4', 11: '3', 12: '2'}
		for i in xrange(0,13):
			labels[i] = id[i]

		plt.scatter(x,y, color = 'gray')
		ax.set_xticklabels(labels)
		ax.set_yticklabels(labels)
		plt.show()
		plt.close()		

	def change_name(self, name): #changes the name of the range and the title of the plot.
		self.name = str(name)
		plt.title(self.name)

	def specific(self, A, B): #marks a specific hand, [x][y]
			self.range[self.translate(A)][self.translate(B)] = 1