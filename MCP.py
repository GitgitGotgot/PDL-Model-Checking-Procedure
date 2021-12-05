import numpy as np
import random
from PropParser import PDLparser
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
"""
Adj_M = {}
Adj_M['START'] = np.array([[0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0]], dtype=bool)
Adj_M['a'] = np.array([[0,1,0,0,0],
              [0,1,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0]], dtype=bool)
Adj_M['b'] = np.array([[0,0,0,0,0],
              [0,0,1,1,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0]], dtype=bool)
Adj_M['c'] = np.array([[0,0,0,0,1],
              [0,0,0,0,1],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0]], dtype=bool)
# Adj_M['a'] = np.array([[0,1,1],
#                        [0,0,0],
#                        [0,0,0]], dtype=bool)
State_V = {}
State_V['p'] = np.array([0,1,0,1,0], dtype=bool)
State_V['q'] = np.array([0,1,1,0,1], dtype=bool)
# State_V['q'] = np.array([0,1,0], dtype=bool)
class Kripke:
    def __init__(self, Adj_M, State_V):
        self.Adj_M = Adj_M
        self.State_V = State_V
        self.atoms = State_V.keys()
        self.programs = Adj_M.keys()
    def Input_Function(self, input_formula):
        """

        """
        formula = PDLparser(self.atoms, self.programs).parse2(input_formula)
        self.MCP(formula)
        # return any true from MCP

    def MCP(self, formula):
        if isinstance(formula, list):
            if len(formula) == 1:
                return self.MCP(formula[0])
            if formula[0] == '<':
                # prog x formula diamond version and box version
                print('formula')
                print(self.MCP(formula[2]).astype(int))
                print('prog')
                print(self.Prog(formula[1]).astype(int))
                print('ret')
                print(self.diamond_op(self.Prog(formula[1]), self.MCP(formula[2])).astype(int))
                return self.diamond_op(self.Prog(formula[1]), self.MCP(formula[2]))
            if formula[0] == '[':
                print('formula')
                print((self.MCP(formula[2])^1).astype(int))
                print('prog')
                print((self.Prog(formula[1])).astype(int))
                print('ret')
                print((self.diamond_op(self.Prog(formula[1]), self.MCP(formula[2])^1)^1).astype(int))
                return self.diamond_op(self.Prog(formula[1]), self.MCP(formula[2])^1)^1
            if formula[0] == '!':
                return self.MCP(formula[1])^1
            if formula[1] == '&':
                #print(self.MCP(formula[0]) & self.MCP(formula[2]))
                return self.MCP(formula[0]) & self.MCP(formula[2])
        else:
            return State_V[formula]

    def Prog(self, program):
        #print('program:', program)
        if isinstance(program, list):
            if len(program) == 1:
                return self.Prog(program[0])
            if program[0] == '!':
                return self.Prog(program[1])^1
            if program[0] == '+':
                prog = self.Prog(program[1])
                return self.kleene_plus(prog)
            if program[0] == '*':
                prog = self.Prog(program[1])
                return np.identity(len(prog), dtype=bool) | self.kleene_plus(prog)
            if program[1] == ';':
                return self.m_composition(self.Prog(program[0]), self.Prog(program[2]))
            if program[1] == 'U':
                return self.Prog(program[0]) | self.Prog(program[2])
        else:
            return self.Adj_M[program]

    def m_composition(self, m1, m2):
        for i in range(len(m1)):
            if not 1 in m1[i]:
                m2[i].fill(0)
        return m2

    def diamond_op(self, m1, v1):
        ret = np.zeros((len(v1)), dtype=bool)
        for i in range(len(m1)):
            for j in range(len(m1[i])):
                ret[i] = ret[i] | (m1[i][j] & v1[j])
        return ret
    def kleene_plus(self, program):
        prog = program
        ret = program
        for i in range(random.randint(1, 20)):
            prog = self.m_composition(prog, program)
            ret = ret | prog
        return ret

k = Kripke(Adj_M, State_V)
while True:
    s = input("Enter a logical formula: ")
    k.Input_Function(s)
