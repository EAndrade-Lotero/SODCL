# Simulation of probabilistic heuristic for WSLS and FRA solving "Seeking the unicorn" task
# Edgar Andrade-Lotero 2020
# Run with Python 3

import run_model as RM

##########################################################################
#
#  Simulation starts here
#
##########################################################################

# Create experiment
p = 0.5 # probability of there being a unicorn
pl = 2 # number of players
n = 8 # number of rows/columns in grid
rounds = 10 # number of rounds
dyads = 100 # number of dyads
gameParameters = [p, pl, n, rounds, dyads]

modelParameters = [0.077, 0.048, 0, 0, 48, 402, 0.99, 1000, 1, 3] # Attractor to ALL
modelParameters += modelParameters # Replicate second player

RM.standard_simulation(gameParameters, modelParameters, DEB=False)
