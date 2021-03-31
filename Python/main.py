# Simulation of probabilistic heuristic for WSLS and FRA solving "Seeking the unicorn" task
# Edgar Andrade-Lotero 2021
# Run with Python 3

print('Importing packages...')
import EmergenceDCL as DL
import Measures
import pandas as pd
import os
print('Done!')

##########################################################################
#
#  Simulation starts here
#
##########################################################################

# Create experiment
p = 0.5 # probability of there being an unicorn
Pl = 2 # number of players
Num_Loc = 8 # number of rows/columns in grid
rounds = 60 # number of rounds
dyads = 50 # number of dyads
gameParameters = [p, Pl, Num_Loc, rounds, dyads]
measures = '13'
TO_FILE = True
# non_shaky_hand = 0.88
non_shaky_hand = 1

playerParameters1 =  {'ALL': 0.1} # Bias towards ALL
playerParameters1['NOTHING'] = 0.1 # Bias towards NOTHING
playerParameters1['T-B-L-R'] = 0.1 # Bias towards TOP-BOTTOM-LEFT-RIGHT
playerParameters1['IN-OUT'] = 0.1 # Bias towards IN-OUT
playerParameters1['alpha'] = 100 # How much the focal region augments attractiveness
playerParameters1['beta'] = 30 # Amplitude of the WSLS sigmoid function
playerParameters1['gamma'] = 31 # Position of the WSLS sigmoid function
playerParameters1['delta'] = 0 # How much the added FRA similarities augments attractiveness
playerParameters1['epsilon'] = 0 # Amplitude of the FRA sigmoid function
playerParameters1['zeta'] = 0 # Position of the FRA sigmoid function

# playerParameters2 =  {'ALL': 0.1} # Bias towards ALL
# playerParameters2['NOTHING'] = 0.1 # Bias towards NOTHING
# playerParameters2['T-B-L-R'] = 0.1 # Bias towards TOP-BOTTOM-LEFT-RIGHT
# playerParameters2['IN-OUT'] = 0.1 # Bias towards IN-OUT
# playerParameters2['alpha'] = 100 # How much the focal region augments attractiveness
# playerParameters2['beta'] = 30 # Amplitude of the WSLS sigmoid function
# playerParameters2['gamma'] = 31 # Position of the WSLS sigmoid function
# playerParameters2['delta'] = 100 # How much the added FRA similarities augments attractiveness
# playerParameters2['epsilon'] = 30 # Amplitude of the FRA sigmoid function
# playerParameters2['zeta'] = 0.7 # Position of the FRA sigmoid function
playerParameters2 = playerParameters1.copy()

print("****************************")
print('Starting simulation')
print("****************************")
print('--- Model parameters ----')
print('--- Player 1 ----')
print('Bias towards ALL: ', playerParameters1['ALL'])
print('Bias towards NOTHING: ', playerParameters1['NOTHING'])
print('Bias towards TOP-BOTTOM-LEFT-RIGHT: ', playerParameters1['T-B-L-R'])
print('Bias towards IN-OUT: ', playerParameters1['IN-OUT'])
print('alpha: ', playerParameters1['alpha'])
print('beta: ', playerParameters1['beta'])
print('gamma: ', playerParameters1['gamma'])
print('delta: ', playerParameters1['delta'])
print('epsilon: ', playerParameters1['epsilon'])
print('zeta: ', playerParameters1['zeta'])
print("\n")
print('--- Player 2 ----')
print('Bias towards ALL: ', playerParameters2['ALL'])
print('Bias towards NOTHING: ', playerParameters2['NOTHING'])
print('Bias towards TOP-BOTTOM-LEFT-RIGHT: ', playerParameters2['T-B-L-R'])
print('Bias towards IN-OUT: ', playerParameters2['IN-OUT'])
print('alpha: ', playerParameters2['alpha'])
print('beta: ', playerParameters2['beta'])
print('gamma: ', playerParameters2['gamma'])
print('delta: ', playerParameters2['delta'])
print('epsilon: ', playerParameters2['epsilon'])
print('zeta: ', playerParameters2['zeta'])
print("****************************")
print('--- Game parameters ---')
print('Probability of unicorn: ', gameParameters[0])
print('Number of players: ', gameParameters[1])
print('Grid size: ', str(gameParameters[2]) + ' x ' + str(gameParameters[2]))
print('Number of rounds: ', gameParameters[3])
print('Number of dyads: ', gameParameters[4])
print("\n")

E = DL.Experiment(gameParameters, [playerParameters1, playerParameters2], non_shaky_hand=non_shaky_hand)
if TO_FILE:
        with open('temp.csv', 'w') as dfile:
            dfile.write('index,Dyad,Round,Player,Answer,a11,a12,a13,a14,a15,a16,a17,a18,a21,a22,a23,a24,a25,a26,a27,a28,a31,a32,a33,a34,a35,a36,a37,a38,a41,a42,a43,a44,a45,a46,a47,a48,a51,a52,a53,a54,a55,a56,a57,a58,a61,a62,a63,a64,a65,a66,a67,a68,a71,a72,a73,a74,a75,a76,a77,a78,a81,a82,a83,a84,a85,a86,a87,a88,Score,Joint,Is_there,Strategy\n')
            dfile.close()
        E.df = pd.read_csv('temp.csv')
E.run_simulation()
if TO_FILE:
    E.df = pd.read_csv('temp.csv')
M = Measures.Measuring(data=E.df, Num_Loc=Num_Loc, TOLERANCE=0)
E.df = M.get_measures(measures)
if TO_FILE: os.remove("temp.csv")
E.save()
