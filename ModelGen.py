import numpy as np
import random
from scipy import sparse

"""
file format example:
STATES
5

PROPS
p
0 1 0

q
0 1 1

PROGS
a
0 1 0
0 1 0
0 0 0

b
0 0 1
0 0 1
0 0 0

TESTS
<a;b>(p&!q)
"""

PROPLETTERS = ['p', 'q', 'r', 's', 't', 'u', 'v', 'w',  'x', 'y']
PROGLETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']

def ModelFromFile(file, sparse_matrix=False):
    components = ['STATES', 'PROPS', 'PROGS', 'TESTS']
    mode = None
    name, data = range(2)
    nameOrData = name
    curName = None
    curData = []
    Progs = {}
    Props = {}
    Tests = []
    with open(file, 'r') as f:
        line = f.readline()
        while line:
            if any(line for c in components if c in line):
                mode = line.strip()
            else:
                if mode == 'STATES':
                    if len(line.split()) > 0:
                        states = int(line.strip())
                if mode == 'PROPS':
                    while len(line.strip()) != 0:
                        curName = line.strip()
                        line = f.readline()
                        Props[curName] = np.array(list(map(int, line.split())), dtype=bool)
                        line = f.readline()
                if mode == 'PROGS':
                    while len(line.strip()) != 0:
                        if nameOrData == name:
                            curName = line.strip()
                            nameOrData = data
                            line = f.readline()
                        else:
                            curData.append(list(map(int, line.split())))
                            line = f.readline()
                    if sparse_matrix:
                        Progs[curName] = sparse.csr_matrix(curData, dtype=bool)
                    else:
                        Progs[curName] = np.array(curData, dtype=bool)
                    curData = []
                    nameOrData = name
                if mode == 'TESTS':
                    Tests.append(line.strip())
            line = f.readline()
    if sparse_matrix:
        Progs['IDENTITY'] = sparse.identity(states, dtype=bool, format='csr')
    else:
        Progs['IDENTITY'] = np.identity(states, dtype=bool)
    return states, Props, Progs, Tests

def RandomModel(states=50, props=10, progs=14, sparse_matrix=False):
    PROPLETTERS = ['p', 'q', 'r', 's', 't', 'u', 'v', 'w',  'x', 'y', 'z']
    PROGLETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
    Progs = {}
    Props = {}
    for i in range(props):
        Props[PROPLETTERS[i]] = np.random.choice([0, 1], size=states, p=[.8, .2]).astype(bool)
    if sparse_matrix:
        Progs['IDENTITY'] = sparse.identity(states, dtype=bool, format='csr')
        for i in range(progs):
            Progs[PROGLETTERS[i]] = sparse.random(states, states, density=0.01, dtype=bool, format='csr')
    else:
        Progs['IDENTITY'] = np.identity(states, dtype=bool)
        for i in range(progs):
            Progs[PROGLETTERS[i]] = np.random.choice([0,1], size=(states,states), p=[.8, .2]).astype(bool)
    return Props, Progs

def LineModel(states=50, p_loc=False, sparse_matrix=False):
    Progs = {}
    Props = {}
    Prop = np.zeros(states, dtype=bool)
    # check if user selected a specific state in which p is true, otherwhise the last state is selected
    if p_loc:
        Prop[int(p_loc)] = True
    else:
        Prop[states-1] = True
    Props['p'] = Prop
    if sparse_matrix:
        Progs['IDENTITY'] = sparse.identity(states, dtype=bool, format='csr')
        Progs['a'] = sparse.eye(states, k=1, dtype=bool, format='csr')
        #print(sparse.eye(states, k=1, dtype=bool, format='csr').A)
    else:
        Progs['IDENTITY'] = np.identity(states, dtype=bool)
        Progs['a'] = np.eye(states, k=1, dtype=bool)
    return Props, Progs

def CircleModel(states=50, p_loc=False, sparse_matrix=False):
    Progs = {}
    Props = {}
    Prop = np.zeros(states, dtype=bool)
    # check if user selected a specific state in which p is true, otherwhise the last state is selected
    if p_loc:
        Prop[int(p_loc)] = True
    else:
        Prop[states-1] = True
    Props['p'] = Prop
    if sparse_matrix:
        Progs['IDENTITY'] = sparse.identity(states, dtype=bool, format='csr')
        M = sparse.eye(states, k=1, dtype=bool, format='csr')
        M[-1, 0] = True
        Progs['a'] = M
        #print(M.A)
    else:
        Progs['IDENTITY'] = np.identity(states, dtype=bool)
        M = np.eye(states, k=1, dtype=bool)
        M[-1, 0] = True
        Progs['a'] = M
    return Props, Progs

def GridModel(states=7, p_loc=False, sparse_matrix=False):
    Progs = {}
    Props = {}
    N = states*states
    Prop = np.zeros(N, dtype=bool)
    # check if user selected a specific state in which p is true, otherwhise the last state is selected
    if p_loc:
        Prop[int(p_loc)] = True
    else:
        Prop[N-1] = True
    Props['p'] = Prop
    Progs['IDENTITY'] = sparse.identity(N, dtype=bool, format='csr') if sparse_matrix else np.identity(N, dtype=bool)
    A = np.eye(N, k=1, dtype=bool)
    for i in range(states-1, N, states):
        # print(A)
        A[i] = np.zeros(N, dtype=bool)
    Progs['a'] = sparse.csr_matrix(A) if sparse_matrix else A
    Progs['b'] =  sparse.eye(N, k=states, dtype=bool, format='csr') if sparse_matrix else np.eye(N, k=states, dtype=bool)
    # print(Progs['a'].A.astype(int))
    # print(Progs['b'].A.astype(int))
    return Props, Progs

def ModelGen(file=False, random_gen=False, line_gen=False, circle_gen=False, states=50, props=10, progs=15, sparse_matrix=False):
    components = ['STATES', 'PROPS', 'PROGS', 'TESTS']
    mode = None
    name, data = range(2)
    nameOrData = name
    curName = None
    curData = []
    Progs = {}
    Props = {}
    Tests = []
    if file:
        with open(file, 'r') as f:
            line = f.readline()
            while line:
                if any(line for c in components if c in line):
                    mode = line.strip()
                else:
                    if mode == 'STATES':
                        if len(line.split()) > 0:
                            states = int(line.strip())
                    if mode == 'PROPS':
                        while len(line.strip()) != 0:
                            curName = line.strip()
                            line = f.readline()
                            Props[curName] = np.array(list(map(int, line.split())), dtype=bool)
                            line = f.readline()
                    if mode == 'PROGS':
                        while len(line.strip()) != 0:
                            if nameOrData == name:
                                curName = line.strip()
                                nameOrData = data
                                line = f.readline()
                            else:
                                curData.append(list(map(int, line.split())))
                                line = f.readline()
                        if sparse_matrix:
                            Progs[curName] = sparse.csr_matrix(curData, dtype=bool)
                        else:
                            Progs[curName] = np.array(curData, dtype=bool)
                        curData = []
                        nameOrData = name
                    if mode == 'TESTS':
                        Tests.append(line.strip())
                line = f.readline()
    elif random_gen:
        for i in range(props):
            Props[PROPLETTERS[i]] = np.random.choice([0, 1], size=states, p=[.8, .2]).astype(bool)
        if sparse_matrix:
            for i in range(progs):
                Progs[PROGLETTERS[i]] = sparse.random(states, states, density=0.01, dtype=bool, format='csr')

        else:
            for i in range(progs):
                Progs[PROGLETTERS[i]] = np.random.choice([0,1], size=(states,states), p=[.8, .2]).astype(bool)
    elif line_gen:
        if sparse_matrix:
            for i in range(props):
                Props[PROPLETTERS[i]] = np.random.choice([0, 1], size=states, p=[.8, .2]).astype(bool)
            Progs['a'] = sparse.eye(states, k=1, dtype=bool, format='csr')
            #print(sparse.eye(states, k=1, dtype=bool, format='csr').A)
        else:
            for i in range(props):
                Props[PROPLETTERS[i]] = np.random.choice([0, 1], size=states, p=[.8, .2]).astype(bool)
            Progs['a'] = np.eye(states, k=1, dtype=bool)
            #print(np.eye(states, k=1, dtype=bool))
    elif circle_gen:
        if sparse_matrix:
            for i in range(props):
                Props[PROPLETTERS[i]] = np.random.choice([0, 1], size=states, p=[.8, .2]).astype(bool)
            M = sparse.eye(states, k=1, dtype=bool, format='csr')
            M[-1, 0] = True
            Progs['a'] = M
            #print(M.A)
        else:
            for i in range(props):
                Props[PROPLETTERS[i]] = np.random.choice([0, 1], size=states, p=[.8, .2]).astype(bool)
            M = np.eye(states, k=1, dtype=bool)
            M[-1, 0] = True
            Progs['a'] = M
            #print(M)
    if sparse_matrix:
        Progs['IDENTITY'] = sparse.identity(states, dtype=bool, format='csr')
    else:
        Progs['IDENTITY'] = np.identity(states, dtype=bool)
    return states, Props, Progs, Tests
