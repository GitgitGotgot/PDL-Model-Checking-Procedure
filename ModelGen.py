import numpy as np
import random
from scipy import sparse

PROPLETTERS = ['p', 'q', 'r', 's', 't', 'u', 'v', 'w',  'x', 'y']
PROGLETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
def ModelGen(file=False, gen=False, states=50, props=10, progs=26, sparse_matrix=False):
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
                            N = int(line.split()[0])
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
    elif gen:
        N = states
        for i in range(props):
            Props[PROPLETTERS[i]] = np.random.choice([0, 1], size=N, p=[.8, .2]).astype(bool)
        if sparse_matrix:
            for i in range(progs):
                Progs[PROGLETTERS[i]] = sparse.random(N, N, density=0.01, dtype=bool, format='csr')

        else:
            for i in range(progs):
                Progs[PROGLETTERS[i]] = np.random.choice([0,1], size=(N,N), p=[.8, .2]).astype(bool)

    if sparse_matrix:
        Progs['IDENTITY'] = sparse.identity(N, dtype=bool, format='csr')
    else:
        Progs['IDENTITY'] = np.identity(N, dtype=bool)
    return N, Props, Progs, Tests
