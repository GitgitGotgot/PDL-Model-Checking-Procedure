# kripke model is already given so we know the atoms
# https://stackoverflow.com/questions/17140850/how-to-parse-a-string-and-return-a-nested-array/17141899#17141899

class PDLparser():
    def __init__(self, atoms, programs):
        self.atoms = atoms
        self.programs = programs
        #self.programs = {'<':[False, '>'], '[':[False, ']']}
        self.open_brac = {'<':False, '[':False, '(':False}
        self.close_brac = {'>':'<', ']':'[', ')':'('}
        self.unary_op = {'!':False, '?':False}
        #self.unary_operators = ['!', '?']
        #self.unary_operators = {'!':False, '?':True}
        self.negation = False
        self.valid_prop_op = ['&']
        self.valid_prog_op = [';','U', '*']
        self.active_program = False
        self.unary_brac = False

    # for future -> operator
    # maybe first strip string into literals [(,q,&,b,),->,c] then iterate
    def parse2(self, i_s):
        stack = [[]]
        for x in i_s:
            if x == '!':
                self.negation = True
            elif x == '<' or x == '[':
                self.open_brac[x] = True
                self.active_program = True
                stack[-1].extend([x,[]])
                stack.append(stack[-1][-1])
                # stack[-1].append([x,[]])
                # stack.append(stack[-1][-1][-1])
            elif x == '>' or x == ']':
                stack.pop()
                if len(stack[-1][-1]) > 3:
                    return 'error: invalid program'
                if not self.open_brac[self.close_brac[x]]:
                    return 'error: misaligned program brackets'
                self.open_brac[self.close_brac[x]] = False
                self.active_program = False
            elif x == '*':
                if not self.active_program:
                    return 'error: program operator used outside program'
                else:
                    stack[-1][-1] = ['*', stack[-1][-1]]
            elif x == '(':
                if self.negation:
                    self.negation = False
                    # stack[-1].extend(['!',[]])
                    # stack.append(stack[-1][-1])
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
                    return 'error: invalid PDLparser'
                #if self.unary_brac:
                    #stack[-1][-1] = ['!', stack[-1][-1]]
                    #self.unary_brac = False
            else:
                if self.active_program and x not in self.valid_prog_op and x not in self.programs:
                    #print(x)
                    return 'error: invalid character in program'
                elif not self.active_program and x not in self.valid_prop_op and x not in self.atoms:
                    #print(x)
                    return 'error: invalid character in formula'
                else:
                    if self.negation:
                        stack[-1].append(['!',x])
                        self.negation = False
                    else:
                        stack[-1].append(x)
        if len(stack) > 1:
            return 'error: closing bracket is missing'
        if len(stack[0]) > 3:
            return 'error: invalid formula'
        return stack.pop()

    def parse_rec(self, i_s):
        def help_func(level=0):
            try:
                token = next(tokens)
                #print(token)
            except StopIteration:
                    return []
            if token == ')' or token == '>' or token == ']':
                if level == 0:
                    raise Exception('missing opening paren')
                else:
                    #if unary_brac:
                        #unary_brac = False
                    return []
            elif token == '(':
                #if unary:
                    #unary = False
                    #return [help_func(level+1, unary_brac=True)] + help_func(level)
                return [help_func(level+1)] + help_func(level)
            elif token == '<' or token == '[':
                return [token, help_func(level+1)] + help_func(level)
            elif token == '!':
                #return [token, help_func(level+1, unary=True)] + help_func(level)
                return [token, help_func(level+1)] + help_func(level)
            else:
                #if unary:
                    #unary = False
                    #return [['!', token]] + help_func(level)
                return [token] + help_func(level)
        tokens = iter(i_s)
        return help_func()
"""
while True:
    c = PDLparser(['p','q','r','s'],['a','b','c','d'])
    # !(p&q) Or (!p & !q)
    s = input("Enter a logical formula: ")
    #ret = c.parse_rec(s)
    ret = c.parse2(s)
    print(ret)
"""
    #print(ret[0])
    #print(ret[0][1])
    #print(ret[0][1][2])
    #print(ret[0][1][2][0])
    #print(ret2[1])
    #print(ret2[1][2])
    #print(c.parse2(s))
    #print(c.foo(s))

#print(foo(s))
# parsed = c.parse("<a>(!p&q)")
# print(parsed)
# <a;(bUc)>p
# [['<>',['a',';',['b', 'U', 'c']]], 'p']
# !p & q
# [['!', 'p'], '&', 'q']
