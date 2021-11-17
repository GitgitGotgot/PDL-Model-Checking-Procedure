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
of parentheses: ‘(φ&ψ)’ is a valid formula, but ‘φ&ψ’ is not and neither is ‘((φ&ψ))’;
likewise, ‘~φ’ is a valid formula but ‘(~φ)’ is not, etc.
"""
