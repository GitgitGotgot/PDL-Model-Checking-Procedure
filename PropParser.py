"""
Logical formula represented as list in lists
checks length of list:
len == 3 -> middle is logical operator
len = 2 -> first is program
len = 1 -> single proposition
[A, Op, B], [A, Op, [B, Op, C]]
[[<q>, A], Op, [<q>, B]]
\
program for input string into lists
the definition of a propositional formula is very specific about the use
of parentheses: ‘(φ & ψ)’ is a valid formula, but ‘φ & ψ’ is not and neither is ‘((φ & ψ))’;
likewise, ‘~φ’ is a valid formula but ‘(~φ)’ is not, etc.

pi | fi & pi | -pi | [a]pi | <a>pi

from nltk import Tree
t = Tree.fromstring('(-pi & fi)')
t.pretty_print()
"""

# kripke model is already given so we know the atoms
# https://stackoverflow.com/questions/17140850/how-to-parse-a-string-and-return-a-nested-array/17141899#17141899
# make unary and proposition 1 input_string
# make program one string

class Formula():
    def __init__(self, atoms):
        self.atoms = atoms
        #self.programs = {'<':[False, '>'], '[':[False, ']']}
        self.open_brac = {'<':False, '[':False, '(':True}
        self.close_brac = {'>':'<', ']':'[', ')':'('}
        #self.unary_operators = ['!', '?']
        #self.unary_operators = {'!':False, '?':True}
        self.unary = False
        self.unary_brac = False
    def parse(self, i_s):
        stack = [[]]
        for x in i_s:
            if x == '!':
                self.unary = True
            elif x == '<' or x == '[':
                self.open_brac[x] = True
                stack[-1].append([x,[]])
                stack.append(stack[-1][-1][-1])
            elif x == '(':
                if self.unary:
                    self.unary_brac = True
                    self.unary = False
                stack[-1].append([])
                stack.append(stack[-1][-1])
            elif x == ')':
                stack.pop()
                if not stack:
                    return 'error: opening bracket is missing'
                if self.unary_brac:
                    stack[-1][-1] = ['!', stack[-1][-1]]
                    self.unary_brac = False
            elif x == '>' or x == ']':
                stack.pop()
                if not self.open_brac[self.close_brac[x]]:
                    return 'error: misaligned program brackets'
            else:
                if self.unary:
                    stack[-1].append(['!',x])
                    self.unary = False
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
                print(token)
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

# have dict with true values to check for opening and closing brackets and unary operator handling
    def parse_rec2(self, s):
        def foo_helper(level=0):
            try:
                token = next(tokens)
            except StopIteration:
                return []
            if token == ']' or token == '>' or token == ')':
                return []
            elif token == '(':
                return [foo_helper(level+1)] + foo_helper(level)
            elif token == '<' or token == '[' or token == '!' or token == '?':
                return [token, foo_helper(level+1)] + foo_helper(level)
            else:
                return [token] + foo_helper(level)
        tokens = iter(s)
        return foo_helper()
"""
    def parse3(self, xs):
        for i, s in enumerate(xs):
            print(s)
            if isinstance(s, list):
                xs[i] = self.parse3(s)
            elif s == '<' or '[' or '!':
                xs[i] = [s, [self.parse3(xs[i+1:])]]
            elif s == '>' or ']':
                return xs.append(xs[i+1:])
            else:
                return xs
    def parse2(self, xs):
        stack = [[]]
        for x in xs:
            if x == '(':
                stack[-1].append([])
                stack.append(stack[-1][-1])
            elif x == ')':
                stack.pop()
                if not stack:
                    return 'error: opening bracket is missing'
                #else:
                    #stack[-1][-1] = parse3(stack[-1][-1])
                    #raise ValueError('error: opening bracket is missing')
            else:
                stack[-1].append(x)
        if len(stack) > 1:
            return 'error: closing bracket is missing'
            #raise ValueError('error: closing bracket is missing')
        return self.parse3(stack.pop())
    def parse_input(self, i_s):
        def parser(k=0, unary=False):
            if unary:
                temp = [unary,[]]
            else:
                temp = ret
            for i in range(k, len(i_s)):
                if i_s[i] == '(':
                    temp[-1].append([])
                    temp.append(temp[-1][-1])
                elif i_s[i] == ')':
                    temp.pop()
                    if not temp:
                        return 'error: opening parentheses bracket is missing'
                elif i_s[i] == '!' or i_s[i] == '<' or i_s[i] == '[':
                    temp[-1].append(parser(i+1, i_s[i]))
                elif i_s[i] == '>' or i_s[i] == ']':
                    if unary:
                        return temp
                    else:
                        return 'error: opening program bracket is missing'
                else:
                    temp[-1].append(x)
                return temp
        ret = [[]]
        ret = parser()
        return ret
    def parse(self, i_s):
        stack = [[]]
        unary = False
        program = False
        for x in i_s:
            if x == '!':
                unary = True
            elif x == '<' or x == '[':
                program = True
                prog = [x,[]]
                #stack[-1].append(x)
            elif x == '(':
                if program:
                    #print(prog)
                    prog[-1].append([])
                    #print(prog)
                    prog.append(prog[-1][-1])
                else:
                    stack[-1].append([])
                    stack.append(stack[-1][-1])
            elif x == ')':
                if program:
                    #print(prog)
                    prog.pop()
                    if not prog:
                        return 'error: opening bracket is missing'
                else:
                    stack.pop()
                    if not stack:
                        return 'error: opening bracket is missing'
                    #raise ValueError('error: opening bracket is missing')
            elif x == '>' or x == ']':
                program = False
                stack[-1].append(prog)
            else:
                if unary and not program:
                    stack[-1].append(['!', x])
                    unary = False
                elif program:
                    if unary:
                        prog[-1].append(['!', x])
                        unary = False
                    else:
                        prog[-1].append(x)
                else:
                    stack[-1].append(x)
        #if len(stack) > 1:
            #return 'error: closing bracket is missing'
            #raise ValueError('error: closing bracket is missing')
        return stack.pop()
    def foo(self, s):
        def foo_helper(level=0):
            try:
                token = next(tokens)
            except StopIteration:
                if level != 0:
                    raise Exception('missing closing paren')
                else:
                    return []
            if token == ')' or token == '>':
                if level == 0:
                    raise Exception('missing opening paren')
                else:
                    return []
            elif token == '(':
                return [foo_helper(level+1)] + foo_helper(level)
            elif token == '<':
                return [token, foo_helper(level+1)] + foo_helper(level)
            else:
                return [token] + foo_helper(level)
        tokens = iter(s)
        return foo_helper()
"""

while True:
    c = Formula(['p','q'])
    # !(p&q) Or (!p & !q)
    s = input("Enter a logical formula: ")
    ret = c.parse(s)
    print(ret)
    #print(ret[0])
    #print(ret[0][1])
    #print(ret[0][1][2])
    #print(ret[0][1][2][0])
    print(c.parse_rec2(s))
    #print(c.parse2(s))
    #print(c.foo(s))

#print(foo(s))
# parsed = c.parse("<a>(!p&q)")
# print(parsed)
# <a;(bUc)>p
# [['<>',['a',';',['b', 'U', 'c']]], 'p']
# !p & q
# [['!', 'p'], '&', 'q']
