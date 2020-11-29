# Simulation of probabilistic heuristic for WSLS and FRA solving "Seeking the unicorn" task
# Edgar Andrade-Lotero 2019
# Run with Python 3

print('Importing packages...')
import numpy as np
import pandas as pd
import EmergenceDCL as DL
import Measures as M
import os
print('Done!')

##########################################################################
# DEFINE FUNCTIONS
##########################################################################

def standard_simulation(gameParameters, modelParameters, TO_FILE=True, DEB=False):

    print("****************************")
    print('Starting simulation')
    print("****************************")
    print('--- Game parameters ---')
    print('Probabilit of a unicorn: ', gameParameters[0])
    print('Number of players: ', gameParameters[1])
    print('Grid size: ', str(gameParameters[2]) + ' x ' + str(gameParameters[2]))
    print('Number of rounds: ', gameParameters[3])
    print('Number of dyads: ', gameParameters[4])
    print("\n")
    print('--- Model parameters ----')
    print('wALL: ', modelParameters[0])
    print('wNOTHING: ', modelParameters[1])
    print('wFAIR_FOCALS: ', modelParameters[2])
    print('wIN_OUT: ', modelParameters[3])
    print('alpha: ', modelParameters[4])
    print('beta: ', modelParameters[5])
    print('gamma: ', modelParameters[6])
    print('delta: ', modelParameters[7])
    print('epsilon: ', modelParameters[8])
    print('zeta: ', modelParameters[9])
    print("\n")

    E = DL.Experiment(gameParameters, modelParameters)
    # Inicializa archivo temporal
    if TO_FILE:
        with open('./data/temp.csv', 'w') as dfile:
            dfile.write('index,Dyad,Round,Player,Answer,Time,a11,a12,a13,a14,a15,a16,a17,a18,a21,a22,a23,a24,a25,a26,a27,a28,a31,a32,a33,a34,a35,a36,a37,a38,a41,a42,a43,a44,a45,a46,a47,a48,a51,a52,a53,a54,a55,a56,a57,a58,a61,a62,a63,a64,a65,a66,a67,a68,a71,a72,a73,a74,a75,a76,a77,a78,a81,a82,a83,a84,a85,a86,a87,a88,Score,Joint,Is_there,where_x,where_y,Strategy\n')
            dfile.close()
    E.run_simulation(TO_FILE=TO_FILE, DEB=DEB)
    if TO_FILE:
        E.df = pd.read_csv('./data/temp.csv')
    E.df = M.get_measures(E.df, '4')
    count = 0
    archivo = './data/output' + str(count) + '.csv'
    while os.path.isfile(archivo):
        count += 1
        archivo = './data/output' + str(count) + '.csv'
    E.df.to_csv(archivo, index=False)
    print('Data saved to' + archivo)

    return E.df
