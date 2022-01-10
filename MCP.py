import numpy as np
from scipy import sparse
from PropParser import PDLparser
from ModelGen import ModelGen

"""
kript struct:
Adj_M = {program key: adjacency matrix}
State_V = {proposition key: interpretation vec}
first make model checking for hardcoded kripke model
function that returns all possible adjacency matrices after program
function that checks if formula is valid in current adjacency matrix

<a>] leads to list index out of range
[a;b*](q&!p)
'NoneType'
<!a> wordt [<,[]]

a.multiply(b) #AND
a+b           #OR
(a>b)+(a<b)   #XOR
a>b           #NOT
"""

class Kripke:
    def __init__(self, Adj_M, State_V, N):
        self.Adj_M = Adj_M
        self.State_V = State_V
        self.atoms = State_V.keys()
        self.programs = Adj_M.keys()
        self.states = N
    def Input_Function(self, input_formula=False, tests=False):
        formula = PDLparser(self.atoms, self.programs).parse(input_formula)
        print('test: ', formula)
        self.MCP(formula)

    def MCP(self, formula):
        if isinstance(formula, list):
            if len(formula) == 1:
                return self.MCP(formula[0])
            if formula[0] == '<':
                print('formula')
                print(self.MCP(formula[2]).astype(int))
                print('prog')
                print(self.Prog(formula[1]).astype(int))
                print('ret')
                # print((self.Prog(formula[1]) @ self.MCP(formula[2])).astype(bool))
                # print(self.Prog(formula[1]).shape + self.MCP(formula[2]).shape)
                print('')
                #return self.diamond_op(self.Prog(formula[1]), self.MCP(formula[2]))
                return (self.Prog(formula[1]) @ self.MCP(formula[2])).astype(bool)
            if formula[0] == '[':
                # print('formula')
                # print((self.MCP(formula[2])^1).astype(int))
                # print('prog')
                # print((self.Prog(formula[1])).astype(int))
                # print('ret')
                print(((self.Prog(formula[1]) @ self.MCP(formula[2])^1)^1).astype(bool))
                print('')
                #return (self.diamond_op(self.Prog(formula[1]), self.MCP(formula[2])^1)^1).astype(bool)
                return ((self.Prog(formula[1]) @ self.MCP(formula[2])^1).astype(bool)^1).astype(bool)
            if formula[0] == 'R':
                prog = self.Prog(formula[1])
                if sparse.issparse(prog):
                    return prog.diagonal()
                return np.diag(prog)
            if formula[0] == 'L':
                prog = self.kleene_plus(self.Prog(formula[1])).astype(bool)
                if sparse.issparse(prog):
                    # print('s[arse]')
                    # print(np.diag(prog).shape)
                    # print((self.Adj_M['IDENTITY'] + prog).shape)
                    # bla = (self.Adj_M['IDENTITY'] + prog) @ np.diag(prog)
                    # print(bla.shape)
                    return ((self.Adj_M['IDENTITY'] + prog).astype(bool) @ prog.diagonal()).astype(bool)
                #print(((self.Adj_M['IDENTITY'] + prog).astype(bool) @ np.diag(prog)).astype(bool))
                # print('donse')
                # print(prog.diagonal().shape)
                # print((self.Adj_M['IDENTITY'] + prog).shape)
                # bla = (self.Adj_M['IDENTITY'] + prog) @ prog.diagonal()
                # bla = np.squeeze(bla)
                # print(bla.shape)
                return ((self.Adj_M['IDENTITY'] + prog).astype(bool) @ np.diag(prog)).astype(bool)
            if formula[0] == '!':
                return (self.MCP(formula[1])^1).astype(bool)
            if formula[1] == '&':
                return (self.MCP(formula[0]) * self.MCP(formula[2])).astype(bool)
            if formula[1] == '/':
                return (self.MCP(formula[0]) + self.MCP(formula[2])).astype(bool)
            if formula[1] == '->':
                return ((self.MCP(formula[0])^1).astype(bool) + self.MCP(formula[2])).astype(bool)
        else:
            print(State_V[formula])
            return State_V[formula]

    def Prog(self, program):
        if isinstance(program, list):
            if len(program) == 1:
                return self.Prog(program[0])
            if program[0] == '!':
                prog = self.Prog(program[1])
                if sparse.issparse(prog):
                    return (prog.A^1).astype(bool)
                return (prog^1).astype(bool)
            if program[0] == "'":
                return self.Prog(program[1]).transpose()
            if program[0] == '+':
                prog = self.Prog(program[1])
                return self.kleene_plus(prog)
            if program[0] == '*':
                prog = self.Prog(program[1]).astype(bool)
                return (self.Adj_M['IDENTITY'] + self.kleene_plus(prog)).astype(bool)
            if program[0] == '?':
                return np.diag(self.MCP(program[1]))
            if program[1] == ';':
                return (self.Prog(program[0]) @ self.Prog(program[2])).astype(bool)
            if program[1] == 'U':
                return (self.Prog(program[0]) + self.Prog(program[2])).astype(bool)
            if program[1] == 'X':
                return (self.Prog(program[0]) * self.Prog(program[2])).astype(bool)
        else:
            return self.Adj_M[program]

    def kleene_plus(self, program):
        prog = program
        ret = program
        # for i in range(random.randint(1, 20)):
        for i in range(self.states^2):
            prog = (prog @ program).astype(bool)
            ret = (ret + prog).astype(bool)
        return ret.astype(bool)

#N, State_V, Adj_M, Tests = ModelGen(file='Test.txt', sparse_matrix=False)
#N, State_V, Adj_M, Tests = ModelGen(gen=True, sparse_matrix=True)
N, State_V, Adj_M, Tests = ModelGen(gen=True, states=100, progs = 3, props = 3, sparse_matrix=True)
# N, State_V, Adj_M, Tests = ModelGen(gen=True, sparse_matrix=True)
Adj_M2 = {}
for key in Adj_M.keys():
    Adj_M2[key] = Adj_M[key].A
    # print(Adj_M2[key].shape)
k2 = Kripke(Adj_M2, State_V, N)
k = Kripke(Adj_M, State_V, N)
while True:
    s = input("Enter a logical formula: ")
    if s == 'T':
        if len(Tests) == 0:
            print('Model has no available tests')
        for t in Tests:
            k.Input_Function(t)
    elif s == 'H':
        print("(Nested) formulas must always be between parentheses\n"
              "Program operators between program brackets (<...> or [...])\n"
              "EXAMPLE: <a;(bUc)>(p->q)\n\n"
              "Formula Operators:\n"
              "Loop = L(insert_program)\n"
              "Repeat = R(insert_program)\n"
              "Logical OR = /\n"
              "Program Operators:\n"
              "Test = (insert_formula)?\n"
              "Disjuntion = X\n\n"
              "To run all tests in the Kripke model file, insert 'T' "
             )
    else:
        #k.Input_Function(s)
        print(k.Input_Function(s) == k2.Input_Function(s))
