import numpy as np

def ModelGen(file):
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
                    N = line.split()
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
                    Progs[curName] = np.array(curData, dtype=bool)
                    curData = []
                    nameOrData = name
                if mode == 'TESTS':
                    Tests.append(line.strip())
            line = f.readline()
    return Props, Progs, Tests
    # print(Props)
    # print(Progs)
    # print(Tests)

# ModelGen('Test.txt')
