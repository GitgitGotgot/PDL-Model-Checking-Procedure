# kripke model is already given so we know the atoms
# https://stackoverflow.com/questions/17140850/how-to-parse-a-string-and-return-a-nested-array/17141899#17141899

# ! is logical negation (and the only unary operator)/NOT
# & is logical conjunction/AND
# / is logical disjunction/OR
#
# * is kleene star operator
# + is kleene plus operator
# ? is test unary_operators
# ' is complement

class PDLparser():
    def __init__(self, atoms, programs):
        self.atoms = atoms
        self.programs = programs
        self.open_brac = {'<':False, '[':False, '(':False}
        self.close_brac = {'>':'<', ']':'[', ')':'('}
        self.unary_op = {'!':False, '?':False}
        self.imp_arrow = False
        self.negation = False
        self.valid_prop_op = ['&', '/']
        self.valid_prog_op = [';','U', 'X', 'R', 'L']
        self.active_program = False

    def parse(self, i_s):
        stack = [[]]
        for x in i_s:
            if x == '!':
                self.negation = True
            elif x == '-':
                if self.imp_arrow:
                    return 'error: invalid formula, expected implication arrow due to -'
                self.imp_arrow = True
            elif x == '<' or x == '[':
                self.open_brac[x] = True
                self.active_program = True
                stack[-1].extend([x,[]])
                stack.append(stack[-1][-1])
            elif x == '>' or x == ']':
                if self.imp_arrow and x == '>':
                    stack[-1].append('->')
                    self.imp_arrow = False
                else:
                    stack.pop()
                    if len(stack[-1][-1]) > 3:
                        return 'error: to many arguments between parentheses'
                    if not self.open_brac[self.close_brac[x]]:
                        return 'error: misaligned program brackets'
                    self.open_brac[self.close_brac[x]] = False
                    self.active_program = False
            elif x == '+' or x == '*' or x == '?' or x == "'":
                if not self.active_program:
                    return 'error: program operator used outside program'
                else:
                    stack[-1][-1] = [x, stack[-1][-1]]
            elif x == '(':
                if self.negation:
                    self.negation = False
                    stack[-1].append(['!',[]])
                    stack.append(stack[-1][-1][-1])
                else:
                    stack[-1].append([])
                    stack.append(stack[-1][-1])
            elif x == ')':
                stack.pop()
                if not stack:
                    return 'error: opening bracket is missing'
                if len(stack[-1][-1]) > 3:
                    return 'error: to many arguments between parentheses'
            else:
                # if self.active_program and x not in self.valid_prog_op and x not in self.programs and x not in self.atoms:
                #     return 'error: invalid character in program'
                # elif not self.active_program and x not in self.valid_prop_op and x not in self.atoms:
                #     return 'error: invalid character in formula'
                # if self.imp_arrow:
                #     return 'error: invalid formula, expected implication arrow due to -'
                # else:
                if self.negation:
                    stack[-1].append(['!', x])
                    self.negation = False
                else:
                    stack[-1].append(x)
        if len(stack) > 1:
            return 'error: closing bracket is missing'
        if len(stack[0]) > 3:
            return 'error: invalid formula'
        return stack.pop()

"""
while True:
    c = PDLparser(['p','q','r','s'],['a','b','c','d'])
    # !(p&q) Or (!p & !q)
    s = input("Enter a logical formula: ")
    #ret = c.parse_rec(s)
    ret = c.parse(s)
    print(ret)
"""
