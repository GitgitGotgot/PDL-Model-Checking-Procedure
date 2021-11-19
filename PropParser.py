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
# PL Precedances
NOT_OPERATOR = 1
AND_OPERATOR = 2
OR_OPERATOR = 3

# kripke model is already given so we know the atoms
# https://stackoverflow.com/questions/17140850/how-to-parse-a-string-and-return-a-nested-array/17141899#17141899
# make negation and proposition 1 input_string
# make program one string
class Formula():
    def __init__(self, atoms):
        self.atoms = atoms
    def parse(self, input_string):
        stack = [[]]
        for x in input_string:
            if x == '(':
                stack[-1].append([])
                stack.append(stack[-1][-1])
            elif x == ')':
                stack.pop()
                if not stack:
                    return 'error: opening bracket is missing'
                    #raise ValueError('error: opening bracket is missing')
            else:
                stack[-1].append(x)
        if len(stack) > 1:
            return 'error: closing bracket is missing'
            #raise ValueError('error: closing bracket is missing')
        return stack.pop()

c = Formula(['p','q'])
# !(p&q) Or (!p & !q)
s = input("Enter a logical formula: ")
print(c.parse(s))
# parsed = c.parse("<a>(!p&q)")
# print(parsed)
# <a;(bUc)>p
# [['<>',['a',';',['b', 'U', 'c']]], 'p']
# !p & q
# [['!', 'p'], '&', 'q']
