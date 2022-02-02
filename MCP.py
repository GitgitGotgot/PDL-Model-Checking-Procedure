import numpy as np
from scipy import sparse
import timeit

class Kripke:
    def __init__(self, Adj_M, State_V, N):
        self.Adj_M = Adj_M
        self.State_V = State_V
        self.atoms = State_V.keys()
        self.programs = Adj_M.keys()
        self.states = N

    def MCP(self, formula):
        if isinstance(formula, list):
            if len(formula) == 1:
                return self.MCP(formula[0])
            if formula[0] == '<':
                return (self.Prog(formula[1]) @ self.MCP(formula[2]))
            if formula[0] == '[':
                return ((self.Prog(formula[1]) @ (self.MCP(formula[2])^1).astype(bool))^1).astype(bool)
            if formula[0] == 'L':
                prog = self.Prog(formula[1])
                if sparse.issparse(prog):
                    return prog.diagonal()
                return np.diag(prog)
            if formula[0] == 'R':
                prog = self.kleene_plus(self.Prog(formula[1])).astype(bool)
                if sparse.issparse(prog):
                    return ((self.Adj_M['IDENTITY'] + prog).astype(bool) @ prog.diagonal())
                return ((self.Adj_M['IDENTITY'] + prog).astype(bool) @ np.diag(prog))
            if formula[0] == '~':
                return ~self.MCP(formula[1])
            if formula[1] == '&':
                return self.MCP(formula[0]) & self.MCP(formula[2])
            if formula[1] == '/':
                return self.MCP(formula[0]) | self.MCP(formula[2])
            if formula[1] == '->':
                return (self.MCP(formula[0]) <= self.MCP(formula[2]))
            if formula[1] == '<->':
                return (self.MCP(formula[0]) & self.MCP(formula[2])) | (~self.MCP(formula[0]) & ~self.MCP(formula[2]))
        else:
            return self.State_V[formula]

    def Prog(self, program):
        if isinstance(program, list):
            if len(program) == 1:
                return self.Prog(program[0])
            if program[0] == '~':
                prog = self.Prog(program[1])
                if sparse.issparse(prog):
                    return (prog.A^1).astype(bool)
                return (prog^1).astype(bool)
            if program[0] == '^':
                return self.Prog(program[1]).transpose()
            if program[0] == '+':
                prog = self.Prog(program[1])
                return self.kleene_plus(prog)
            if program[0] == '*':
                prog = self.Prog(program[1]).astype(bool)
                return (self.Adj_M['IDENTITY'] + self.kleene_plus(prog)).astype(bool)
            if program[0] == '?':
                prog = self.MCP(program[1])
                if sparse.issparse(self.Adj_M['IDENTITY']):
                    return sparse.diags(prog, dtype=bool)
                return np.diag(prog)
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
        for i in range(self.states):
            prog = (prog @ program)
            ret = (ret + prog).astype(bool)
        return ret
