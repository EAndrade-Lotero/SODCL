import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import gridspec
from random import choice, uniform, random, sample, randint, choices

###########################################################
# GLOBAL VARIABLES
###########################################################

TOLERANCIA = 1
DEB = False
IMPR = False

regionsCoded = ['abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789;:', # ALL
                  '', # NOTHING
                  'GHIJKLMNOPQRSTUVWXYZ0123456789;:', # BOTTOM
                  'abcdefghijklmnopqrstuvwxyzABCDEF', # TOP
                  'abcdijklqrstyzABGHIJOPQRWXYZ4567', # LEFT
                  'efghmnopuvwxCDEFKLMNSTUV012389;:', # RIGHT
                  'jklmnorstuvwzABCDEHIJKLMPQRSTUXYZ012', # IN
                  'abcdefghipqxyFGNOVW3456789;:' # OUT
                  ]

regions = ['RS', \
           'ALL', \
           'NOTHING', \
           'BOTTOM', \
           'TOP', \
           'LEFT', \
           'RIGHT', \
           'IN', \
           'OUT']

###########################################################
# FUNCTIONS
###########################################################

def new_random_strategy(Num_Loc=8):
    # Creates a new random strategy to explore grid
    # The size of this new strategy is determined by
    # a normal distribution with mean = m and s.d. = sd
    n = randint(2,Num_Loc * Num_Loc - 2)
    return list(np.random.choice(Num_Loc * Num_Loc, n)) # Probando absolutamente random

def imprime_region(r):
	print(r[0:8])
	print(r[8:16])
	print(r[16:24])
	print(r[24:32])
	print(r[32:40])
	print(r[40:48])
	print(r[48:56])
	print(r[56:64])

def nameRegion(r):
    global regions
    name = regions[r]
    # print(f"Estoy buscando aqui: {regions} este numero {r} y obtengo esto {name}")
    return name

def numberRegion(r):
    global regions
    reg = regions.index(r)
    # print(f"Estoy buscando aqui: {regions} esto {r} y obtengo esto {reg}")
    return reg

def complement(r):
	if r == 'RS':
		return 'RS'
	elif r == 'ALL':
		return 'NOTHING'
	elif r == 'NOTHING':
		return 'ALL'
	elif r == 'BOTTOM':
		return 'TOP'
	elif r == 'TOP':
		return 'BOTTOM'
	elif r == 'LEFT':
		return 'RIGHT'
	elif r == 'RIGHT':
		return 'LEFT'
	elif r == 'IN':
		return 'OUT'
	elif r == 'OUT':
		return 'IN'

def region2strategy(region):
    strategy = []
    for i in range(64):
        if region[i] == 1:
            strategy.append(i)
    return strategy

def lettercode2Strategy(coded, Num_Loc):
	letras = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789;:')
	v = []
	for c in coded:
		v.append(letras.index(c))
	return v

def code2Vector(strategy, Num_Loc):
    size = int(Num_Loc * Num_Loc)
    v = [0] * size
    for i in range(size):
        if i in strategy:
            v[i] = 1
    return v

def create_regions_and_strategies(Num_Loc):
	size = int(Num_Loc * Num_Loc)
	half_size = int(Num_Loc * Num_Loc / 2)
	half_Num_Loc = int(Num_Loc / 2)
	# ALL and NOTHING
	all = [1] * size
	nothing = [0] * size
	# TOP and BOTTOM
	up = [1] * half_size + [0] * half_size
	bottom = [1 - i for i in up]
	# LEFT and RIGHT
	right = []
	for i in range(0, Num_Loc):
		right += [0] * half_Num_Loc + [1] * half_Num_Loc
	left = [1 - i for i in right]
	# IN and OUT
	In = [0] * Num_Loc
	for i in range(Num_Loc - 2):
		In += [0] + [1] * (Num_Loc - 2) + [0]
	In += [0] * Num_Loc
	out = [1 - i for i in In]
	# Define the strategies
	TOP = []
	BOTTOM = []
	LEFT = []
	RIGHT = []
	IN = []
	OUT = []
	ALL = []
	NOTHING = []
	for i in range(int(Num_Loc * Num_Loc)):
		if up[i] == 1:
			TOP.append(i)
		if bottom[i] == 1:
			BOTTOM.append(i)
		if left[i] == 1:
			LEFT.append(i)
		if right[i] == 1:
			RIGHT.append(i)
		if all[i] == 1:
			ALL.append(i)
		if nothing[i] == 1:
			NOTHING.append(i)
		if In[i] == 1:
			IN.append(i)
		if out[i] == 1:
			OUT.append(i)
	strategies = {}
	strategies[0] = list(np.random.choice(Num_Loc * Num_Loc, np.random.randint(Num_Loc * Num_Loc)))
	while len(strategies[0]) < 2 or len(strategies[0]) > 62:
	       strategies[0] = list(np.random.choice(Num_Loc * Num_Loc, np.random.randint(Num_Loc * Num_Loc)))
	strategies[1] = ALL
	strategies[2] = NOTHING
	strategies[3] = BOTTOM
	strategies[4] = TOP
	strategies[5] = LEFT
	strategies[6] = RIGHT
	strategies[7] = IN
	strategies[8] = OUT
	strategies[9] = list(np.random.choice(Num_Loc * Num_Loc, np.random.randint(Num_Loc * Num_Loc)))
	while len(strategies[9]) < 2 or len(strategies[9]) > 62:
	       strategies[9] = list(np.random.choice(Num_Loc * Num_Loc, np.random.randint(Num_Loc * Num_Loc)))
	return [all, nothing, bottom, up, left, right, In, out], strategies

def dibuja_region(reg, Num_Loc):
	assert(len(reg) == Num_Loc * Num_Loc), "Incorrect region size!"
	print(reg)
	fig4, axes4 = plt.subplots()
	axes4.get_xaxis().set_visible(False)
	axes4.get_yaxis().set_visible(False)
	step = 1. / Num_Loc
	tangulos = []
	for j in range(0, Num_Loc * Num_Loc):
		x = int(j) % Num_Loc
		y = (int(j) - x) / Num_Loc
		# print("x: " + str(x + 1))
		# print("y: " + str(y + 1))
		by_x = x * step
		by_y = 1 - (y + 1) * step
		#     # print("by_x: " + str(by_x))
		#     # print("by_y: " + str(by_y))
		if reg[j] == 1:
			tangulos.append(patches.Rectangle(*[(by_x, by_y), step, step],\
			facecolor="black", alpha=1))
	for t in tangulos:
		axes4.add_patch(t)
	plt.show()

def dibuja_regiones(reg1, reg2, Num_Loc, titulo):
	assert(len(reg1) == Num_Loc * Num_Loc), "Incorrect region size 1!"
	assert(len(reg2) == Num_Loc * Num_Loc), "Incorrect region size 2!"
	fig4, axes4 = plt.subplots(1,2)
	for a in axes4:
		a.get_xaxis().set_visible(False)
		a.get_yaxis().set_visible(False)
	step = 1. / Num_Loc
	tangulos1 = []
	tangulos2 = []
	for j in range(0, Num_Loc * Num_Loc):
		x = int(j) % Num_Loc
		y = (int(j) - x) / Num_Loc
		by_x = x * step
		by_y = 1 - (y + 1) * step
		if reg1[j] == 1:
			tangulos1.append(patches.Rectangle(*[(by_x, by_y), step, step],\
			facecolor="black", alpha=1))
		if reg2[j] == 1:
			tangulos2.append(patches.Rectangle(*[(by_x, by_y), step, step],\
			facecolor="black", alpha=1))
		if reg1[j] == 1 and reg2[j] == 1:
			tangulos1.append(patches.Rectangle(*[(by_x, by_y), step, step],\
			facecolor="red", alpha=1))
			tangulos2.append(patches.Rectangle(*[(by_x, by_y), step, step],\
			facecolor="red", alpha=1))
	for t in tangulos1:
		axes4[0].add_patch(t)
	for t in tangulos2:
		axes4[1].add_patch(t)
	fig4.suptitle(titulo)
	plt.show()

def dibuja_ronda(reg1, sco1, reg2, sco2, Num_Loc, modelParameters, focals, titulo):
    assert(len(reg1) == Num_Loc * Num_Loc), "Incorrect region size 1!"
    assert(len(reg2) == Num_Loc * Num_Loc), "Incorrect region size 2!"
    # Initializing Plot
    fig = plt.figure()
    spec = gridspec.GridSpec(ncols=2, nrows=2)#, height_ratios=[3, 1, 1, 1])
    fig.subplots_adjust(left=0.1, bottom=0.05, right=0.9, top=0.95, wspace=0.1, hspace=0.2)
    ax0 = fig.add_subplot(spec[0,0])
    ax1 = fig.add_subplot(spec[0,1])
    ax2 = fig.add_subplot(spec[1,0])
    ax3 = fig.add_subplot(spec[1,1])
    ax0.set_title('Player 1')
    ax1.set_title('Player 2')
    ax0.get_xaxis().set_visible(False)
    ax1.get_xaxis().set_visible(False)
    ax0.get_yaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    ax2.set_yticklabels([])
    ax2.set_ylabel('Number of \n different tiles', fontsize=8)
    ax3.yaxis.tick_right()
    # Ploting regions
    step = 1. / Num_Loc
    tangulos1 = []
    tangulos2 = []
    for j in range(0, Num_Loc * Num_Loc):
        x = int(j) % Num_Loc
        y = (int(j) - x) / Num_Loc
        by_x = x * step
        by_y = 1 - (y + 1) * step
        if reg1[j] == 1:
            tangulos1.append(patches.Rectangle(*[(by_x, by_y), step, step],\
			facecolor="black", alpha=1))
        if reg2[j] == 1:
            tangulos2.append(patches.Rectangle(*[(by_x, by_y), step, step],\
			facecolor="black", alpha=1))
        if reg1[j] == 1 and reg2[j] == 1:
            tangulos1.append(patches.Rectangle(*[(by_x, by_y), step, step],\
			facecolor="red", alpha=1))
            tangulos2.append(patches.Rectangle(*[(by_x, by_y), step, step],\
			facecolor="red", alpha=1))
    for t in tangulos1:
        ax0.add_patch(t)
    for t in tangulos2:
        ax1.add_patch(t)
    # Plot attractiveness
    regions_names = ['RS','A','N','B','T','L','R','I','O']
    # regions_names = ['A','N','B','T','L','R','I','O']
    overlap = np.multiply(reg1, reg2).tolist()
    # frasPL1 = attractiveness(reg1, sco1, overlap, 0, modelParameters, Num_Loc, focals)
    # frasPL2 = attractiveness(reg2, sco2, overlap, 1, modelParameters, Num_Loc, focals)
    # frasPL1 = [dist(reg1, k) for k in focals]
    # frasPL2 = [dist(reg2, k) for k in focals]
    frasPL1 = probabilities(reg1, sco1, overlap, modelParameters, focals, focals)
    frasPL2 = probabilities(reg2, sco2, overlap, modelParameters, focals, focals)
    ax2.set_ylim(0,max(1,max(frasPL1)))
    ax3.set_ylim(0,max(1,max(frasPL2)))
    ax2.bar(regions_names, frasPL1)
    ax3.bar(regions_names, frasPL2)
    threshold = frasPL1[0]
    # threshold = 20
    ax2.axhline(y=threshold, linewidth=1, color='k')
    ax3.axhline(y=threshold, linewidth=1, color='k')
    fig.suptitle(titulo)
    plt.show()

def sigmoid(x, beta, gamma):
    # define attractiveness and choice functions
	return 1. / (1 + np.exp(-beta * (x - gamma)))

def sim_consist(v1, v2):
	# Returns the similarity based on consistency
	# v1 and v2 are two 64-bit coded regions
	if type(v1) == type(np.nan) or type(v2) == type(np.nan):
	       return np.nan
	else:
	       assert(len(v1) == 64), 'v1 must be a 64-bit coded region!'
	       assert(len(v2) == 64), 'v2 must be a 64-bit coded region!'
	       joint = [v1[x] * v2[x] for x in range(len(v1))]
	       union = [v1[x] + v2[x] for x in range(len(v1))]
	       union = [x/x for x in union if x != 0]
	       j = np.sum(np.array(joint))
	       u = np.sum(np.array(union))
	       if u != 0:
	              return float(j)/u
	       else:
	              return 1

def sim(r1, r2, e):
    '''
    Returns similarity based on inverse exponential euclidean distance
    '''
    distance = np.subtract(r1, r2)
    distance = np.multiply(distance, distance)
    distance = np.sqrt(np.sum(distance))
    return np.exp(-e*distance)

def dist(k, i):
    # Returns distance between regions k and i in terms of number of different tiles
    # Input: k, which is a region coded as a vector of 0s and 1s of length 64
    #        i, which is a region coded as a vector of 0s and 1s of length 64
    #        o, which is a parameter for the exponential
    return np.abs(np.subtract(k, i)).sum()

def maxSim2Focal(r, Num_Loc):
    # Returns maximum similarity (BASED ON CONSISTNECY) to focal region
    # Input: r, which is a region coded as a vector of 0s and 1s of length 64
    similarities = [0] * 8
    contador = 0
    for k in regionsCoded:
        reg = lettercode2Strategy(k, Num_Loc)
        kV = code2Vector(reg, Num_Loc)
        # imprime_region(kV)
        # finding similarity to COMPLEMENT
        kComp = [1 - x for x in kV]
        sss = sim_consist(r, kComp)
        # print('Similarity to Comp Region', contador, ' is:', sss)
        similarities[contador] = sss
        contador = contador + 1
    # simPrint = ["%.3f" % v for v in similarities]
    # print('maxSim2Focal', simPrint)
    valor = np.max(np.array(similarities))
    return(valor)

def minDist2Focal(r, regionsCoded):
	# Returns closest distance to focal region
	# Input: r, which is a region coded as a vector of 0s and 1s of length 64
	# Output: number representing the closest distance
	distances = [dist(r, k) for k in regionsCoded]
	return min(distances)

def minDistComp2Focal(r, complements):
	# Returns closest distance to complementary focal region
	# Input: r, which is a region coded as a vector of 0s and 1s of length 64
	# Output: number representing the closest distance
	distances = [dist(r, k) for k in complements]
	# Leave out distance to NOTHING
	distances = distances[1:]
	return min(distances)

def classify_region(r, focals, TOLERANCIA):
	# Returns name of closest region
	# Input: r, which is a region coded as a vector of 0s and 1s of length 64
	distances = [dist(list(r), k) for k in focals]
	valor = np.min(distances)
	indiceMin = np.argmin(distances)
	if valor < TOLERANCIA:
		return(nameRegion(indiceMin + 1))
	else:
		return('RS')

def probabilities(region, score, overlap, modelParameters, focals, strategies, DEB=False, Num_Loc=8):
	global regions
	global TOLERANCIA
	# Determining biases
	wALL = float(modelParameters[0])
	wNOTHING = float(modelParameters[1])
	wBOTTOM = float(modelParameters[2])
	wTOP = float(modelParameters[2])
	wLEFT = float(modelParameters[2])
	wRIGHT = float(modelParameters[2])
	wIN = float(modelParameters[3])
	wOUT = float(modelParameters[3])
	wRS = 1 - np.sum(np.array([wALL, wNOTHING, wBOTTOM, wTOP, wLEFT, wRIGHT, wIN, wOUT]))
	assert(wRS > 0), "Incorrect biases!"
	bias = [wRS, wALL, wNOTHING, wBOTTOM, wTOP, wLEFT, wRIGHT, wIN, wOUT]
	if DEB:
		biasPrint = ["%.3f" % v for v in bias]
		print('bias:\n', biasPrint)
	# Adding 'Win Stay'
	attractiveness = [x for x in bias] # start from bias
	alpha = float(modelParameters[4]) # for how much WSLS augments attractiveness
	beta = float(modelParameters[5]) # steepness of the WSLS sigmoid function
	gamma = float(modelParameters[6]) # threshold of the WSLS sigmoid function
	r = classify_region(region, focals, TOLERANCIA)
	i = numberRegion(r)
	if i != 0:
	          attractiveness[i] += alpha * sigmoid(score, beta, gamma)
	if DEB:
		attactPrint = ["%.3f" % v for v in attractiveness]
		print('attractiveness with WS:\n', attactPrint)
	# Adding similarity to complement
	delta = float(modelParameters[7]) # for how much similarity to complement augments attractiveness
	epsilon = float(modelParameters[8]) # steepness of exponential similarity
	for l in ['NOTHING', 'BOTTOM', 'TOP', 'LEFT', 'RIGHT', 'IN', 'OUT']:
		compl = complement(l)
		k = numberRegion(compl)
		attractiveness[k] += delta * sim(overlap, focals[k - 1], epsilon)
	if DEB:
		attactPrint = ["%.3f" % v for v in attractiveness]
		print('attractiveness with similarity to complement:\n', attactPrint)
    # Adding stubbornness
	zeta = float(modelParameters[9]) # stubbornness
	if i != 0:
		attractiveness[i] += zeta
	if DEB:
		attactPrint = ["%.3f" % v for v in attractiveness]
		print('attractiveness with similarity to focal:\n', attactPrint)
	sum = np.sum(attractiveness)
	probs = [x/sum for x in attractiveness]
	return probs

def estimate_strategy(region, score, overlap, parameters, focals, strategies, DEB=False):
    global regions
    probs = probabilities(region, score, overlap, parameters, focals, strategies, DEB=DEB)
    r = np.random.choice(regions, p=probs)
    if r == 'RS':
        new_strategy = new_random_strategy()
    else:
        new_strategy = strategies[numberRegion(r)]
    if DEB:
        probsPrint = ["%.3f" % v for v in probs]
        # print("Regiones:", regions)
        print("Probabilities:", probsPrint)
        print("Chosen region:", r)
        imprime_region(code2Vector(new_strategy, 8))
    return new_strategy

def shaky_hand(strategy, p=2):
    outs = np.random.choice(strategy, p) if len(strategy) > 0 else []
    complement = [i for i in range(64) if i not in strategy]
    ins = np.random.choice(complement, p) if len(complement) > 0 else []
    strategy = [i for i in strategy if i not in outs] + list(ins)
    return [i for i in strategy]

def calcula_consistencia(x, y):
    joint = np.multiply(x,y)
    total_visited = np.add(x,y)
    total_visited = total_visited.astype(float)
    total_visited = total_visited * 0.5
    total_visited = np.ceil(total_visited)
    j = np.sum(joint)
    t = np.sum(total_visited)
    if t != 0:
        return j/t
    else:
        return 1
