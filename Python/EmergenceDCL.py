# Class definition for solving "Seeking the unicorn" task
# Edgar Andrade-Lotero 2021
# Run with Python 3
# Run from main.py
# Requires FRA.py

from random import choices, uniform, randint
from math import floor
import numpy as np
import pandas as pd
import os
import FRA

DEB = False

#################################
# FUNCTIONS
################################

# Define players
class player :
	'''Object defining a player.'''

	def __init__(self, Ready, Decision, Choice, Where, Joint, Score, Accuracy, Name, modelParameters):
		self.ready = Ready
		self.decision = Decision
		self.choice = Choice
		self.where = Where
		self.joint = Joint
		self.score = Score
		self.accuracy = Accuracy
		self.name = Name
		self.parameters = modelParameters
		self.regionsNames = ['RS', \
		           'ALL', \
		           'NOTHING', \
		           'BOTTOM', \
		           'TOP', \
		           'LEFT', \
		           'RIGHT', \
		           'IN', \
		           'OUT']
		self.regionsCoded = ['abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789;:', # ALL
		                  '', # NOTHING
		                  'GHIJKLMNOPQRSTUVWXYZ0123456789;:', # BOTTOM
		                  'abcdefghijklmnopqrstuvwxyzABCDEF', # TOP
		                  'abcdijklqrstyzABGHIJOPQRWXYZ4567', # LEFT
		                  'efghmnopuvwxCDEFKLMNSTUV012389;:', # RIGHT
		                  'jklmnorstuvwzABCDEHIJKLMPQRSTUXYZ012', # IN
		                  'abcdefghipqxyFGNOVW3456789;:' # OUT
		                  ]
		self.strategies = [FRA.lettercode2Strategy(x, 8) for x in self.regionsCoded]
		self.regions = [FRA.code2Vector(x, 8) for x in self.strategies]
		self.complements = [[1 - x for x in sublist] for sublist in self.regions]

	def make_decision(self, place):
		attractiveness = self.attract(place)
		sum = np.sum(attractiveness)
		probabilities = [x/sum for x in attractiveness]
		newChoice = choices(range(9), weights=probabilities)[0]
		self.choice = newChoice

	def attract(self, place, DEB=False):
		wALL = float(self.parameters['ALL'])
		wNOTHING = float(self.parameters['NOTHING'])
		wBOTTOM = float(self.parameters['T-B-L-R'])
		wTOP = float(self.parameters['T-B-L-R'])
		wLEFT = float(self.parameters['T-B-L-R'])
		wRIGHT = float(self.parameters['T-B-L-R'])
		wIN = float(self.parameters['IN-OUT'])
		wOUT = float(self.parameters['IN-OUT'])
		wRS = 1 - np.sum(np.array([wALL, wNOTHING, wBOTTOM, wTOP, wLEFT, wRIGHT, wIN, wOUT]))
		assert(wRS > 0), "Incorrect biases! Sum greater than 1"

		alpha = float(self.parameters['alpha']) # for how much the focal region augments attractiveness
		beta = float(self.parameters['beta']) # amplitude of the WSLS sigmoid function
		gamma = float(self.parameters['gamma']) # position of the WSLS sigmoid function

		delta = float(self.parameters['delta']) # for how much the added FRA similarities augments attractiveness
		epsilon = float(self.parameters['epsilon']) # amplitude of the FRA sigmoid function
		zeta = float(self.parameters['zeta']) # position of the FRA sigmoid function

		# start from biases
		attractiveness = [wRS, wALL, wNOTHING, wBOTTOM, wTOP, wLEFT, wRIGHT, wIN, wOUT]
		if DEB:
			attactPrint = ["%.3f" % v for v in attractiveness]
			print('Player', self.name)
			print('attractiveness before WS and FRA\n', attactPrint)

		# Adding 'Win Stay'
		if self.choice != 0:
			attractiveness[self.choice] += alpha * FRA.sigmoid(self.score, beta, gamma)

		if DEB:
			attactPrint = ["%.3f" % v for v in attractiveness]
			print('attractiveness with WS\n', attactPrint)

		# Adding 'FRA'
		if place == -1:
			visited = FRA.code2Vector(self.where, 8)
			sims1 = [0] + [FRA.sim_consist(visited, x) for x in self.regions]
			overlap = FRA.code2Vector(self.joint, 8)
			sims2 = [0] + [FRA.sim_consist(overlap, x) for x in self.complements]
			sims2[0] = 0 # ALL's complement, NOTHING, does not repel to ALL
			FRAsims = np.add(sims1, sims2)
			attractiveness = np.add(attractiveness, [delta * FRA.sigmoid(x, epsilon, zeta) for x in FRAsims])

		if DEB:
			attactPrint = ["%.3f" % v for v in attractiveness]
			print('attractiveness with FRA\n', attactPrint)

		return attractiveness

# Define Experiment Object
class Experiment :
	'''Object defining the experiment and simulation'''

	def __init__(self, gameParameters, modelParameters, non_shaky_hand=1):
		assert(len(gameParameters) == 5), "Game parameters incorrect length!"
		self.gameParameters = gameParameters
		self.modelParameters = modelParameters
		self.non_shaky_hand = non_shaky_hand
		# Create data frame
		cols = ['Dyad', 'Round', 'Player', 'Answer']
		cols += ['a' + str(i+1) + str(j+1) for i in range(0, 8) for j in range(0, 8)]
		cols += ['Score', 'Joint', 'Is_there','Strategy']
		self.df = pd.DataFrame(columns=cols)

	def run_dyad(self, TO_FILE=True):

		p = self.gameParameters[0] # probability of there being a unicorn (usually 0.5)
		Pl = self.gameParameters[1] # number of players (usually 2)
		Num_Loc = self.gameParameters[2] # number of locations (squares in a row in the grid; usually 8)
		rounds = self.gameParameters[3] # number of iterations per experiment

		# Create players
		Players = []
		for k in range(0, Pl):
			Players.append(player(False, "", 0, [], [], 0, False, int(uniform(0, 1000000)), self.modelParameters[k]))

		# Start the rounds
		for i in range(0, rounds):
			# Playing round i

			#Initializing players for round
			for pl in Players:
				pl.decision = ""
				pl.where = []
				pl.joint = []
				pl.ready = False
				pl.score = 0
				pl.accuracy = False

			# Determine whether there is a unicorn and where
			place = -1
			if uniform(0, 1) > p:
				place = int(floor(uniform(0, Num_Loc * Num_Loc - 1)))
			
			# Determine players' chosen region
			chosen_strategies = []
			for k in range(0, Pl):
				chosen = Players[k].choice
				if chosen == 0:
					n = randint(2, Num_Loc * Num_Loc - 2)
					chosen_strategies.append(list(np.random.choice(Num_Loc * Num_Loc, n, replace=False)))
				else:
					chosen_strategies.append(Players[k].strategies[chosen - 1])
				chosen_strategies[k] = self.shake(chosen_strategies[k])

			# Start searching for the unicorn
			for j in range(0, Num_Loc * Num_Loc + 1):
				# Running iteration j
				for k in range(0, Pl):
					# Check if other player said present. If so, do the same
					if Players[1 - k].decision == "Present":
						Players[k].decision = "Present"
						Players[k].ready = True
						break
					# If the other player did not say Present, and current player is not ready, then...
					elif not Players[k].ready:
						# ...look at the location determined by the strategy
						# Check if strategy is not over...
						if j<len(chosen_strategies[k]):
							search_place = chosen_strategies[k][j]
							Players[k].where.append(search_place)
							if search_place == place:
								Players[k].decision = "Present"
								Players[k].ready = True
						# Otherwise, say Absent
						else:
							# The strategy is over, so guess Absent
							Players[k].decision = "Absent"
							Players[k].ready = True
					# Check if both players are ready. If so, stop search
					elif Players[1-k].ready == True:
						break
				else:
				# Not finished yet
					continue
				break

			# Get results and store data in dataframe (returns players with updated scores)
			Players = self.round2dataframe(Players, i+1, place, TO_FILE)

			# Determine locations visited by both players
			both = list(set(Players[0].where).intersection(set(Players[1].where)))

			if DEB:
				Is_there = " Absent" if place == -1 else " Present"
				print('-----------------')
				print('Unicorn ' + Is_there)
				print('both', len(both))
				print('scores: p0: ', Players[0].score, ' p1: ', Players[1].score)
				print('End summary round ', i)
				print('-----------------')
				FRA.draw_round(Players[0],Players[1], "Round: " + str(i) + " (" + Is_there + ") Scores: (" + str(Players[0].score) + "," + str(Players[1].score))

			# Players determine their next strategies
			for k in range(0,Pl):
				Players[k].joint = both
				Players[k].make_decision(place)
	
	def shake(self, strategy):
		if uniform(0, 1) > self.non_shaky_hand:
			p = 2
			outs = np.random.choice(strategy, p) if len(strategy) > 0 else []
			complement = [i for i in range(64) if i not in strategy]
			ins = np.random.choice(complement, p) if len(complement) > 0 else []
			return [i for i in strategy if i not in outs] + list(ins)
		else:
			return strategy

	def run_simulation(self):
		iters = self.gameParameters[4] # number of experiments in a set
		for d in range(0, iters):
			print("****************************")
			print("Running dyad no. ", d + 1)
			print("****************************\n")
			self.run_dyad()
	
	def round2dataframe(self, Players, round, place, TO_FILE):
		Num_Loc = self.gameParameters[2]
		# Create row of data as dictionary
		row_of_data = {}
		# Create dyad name
		dyad = ''
		for pl in Players: dyad += str(pl.name)[:5]
		# Determine locations visited by both players
		both = list(set(Players[0].where).intersection(set(Players[1].where)))
		# Save data per player
		for k in range(0, len(Players)):
			# Determine individual scores
			if place == -1:
				# There was NO unicorn
				if Players[k].decision == "Absent":
					# Player k's answer is Correct
					Players[k].accuracy = True
					Players[k].score = Num_Loc*Num_Loc/2 - len(both)
				else:
					# Player k's answer is Incorrect
					Players[k].accuracy = False
					Players[k].score = -Num_Loc*Num_Loc - len(both)
			else:
				# There was an unicorn
				if Players[k].decision == "Present":
					# Player k's answer is Correct
					Players[k].accuracy = True
					Players[k].score = Num_Loc*Num_Loc/2 - len(both)
				else:
					# Player k's answer is Incorrect
					Players[k].accuracy = False
					Players[k].score = -Num_Loc*Num_Loc - len(both)
			row_of_data['Dyad'] = [dyad]
			row_of_data['Round'] = [round]
			row_of_data['Player'] = [Players[k].name]
			row_of_data['Answer'] = [Players[k].decision]
			colA = ['a' + str(i+1) + str(j+1) for i in range(0, Num_Loc) for j in range(0,Num_Loc)]
			for l in range(0, Num_Loc * Num_Loc):
				if l in Players[k].where:
					row_of_data[colA[l]] = [1]
				else:
					row_of_data[colA[l]] = [0]
			row_of_data['Score'] = [Players[k].score]
			row_of_data['Joint'] = [len(both)]
			if place == -1:
				row_of_data['Is_there'] = ["Unicorn_Absent"]
			else:
				row_of_data['Is_there'] = ["Unicorn_Present"]
			row_of_data['Strategy'] = [Players[k].choice]
			# Add data to dataFrame
			dfAux = pd.DataFrame.from_dict(row_of_data)
			# Keeping the order of columns
			dfAux = dfAux[['Dyad','Round','Player','Answer']+colA+['Score','Joint','Is_there','Strategy']]

			if TO_FILE:
				with open('temp.csv', 'a') as f:
					dfAux.to_csv(f, header=False)
			else:
				self.df = self.df.append(dfAux, ignore_index = True)

		return Players

	def save(self):
		count = 0
		file_name = './Data/output' + str(count) + '.csv'
		while os.path.isfile(file_name):
			count += 1
			file_name = './Data/output' + str(count) + '.csv'
		self.df.to_csv(file_name, index=False)
		print('Data saved to ' + file_name)