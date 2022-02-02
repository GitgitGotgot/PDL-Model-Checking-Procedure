# kripke model is already given so we know the atoms
# https://stackoverflow.com/questions/17140850/how-to-parse-a-string-and-return-a-nested-array/17141899#17141899

def FormulaParser(i_s, atoms, programs):
    open_brac = {'<':False, '[':False, '(':False}
    close_brac = {'>':'<', ']':'[', ')':'('}
    imp_arrow = False
    bimp_arrow = False
    negation = False
    valid_prop_op = ['&', '/', 'R', 'L', 'T', 'F']
    valid_prog_op = [';','U', 'X']
    active_program = False
    stack = [[]]
    i_s = i_s.replace(" ", "")
    for x in i_s:
        if x == '~':
            negation = True
        elif x == '-':
            if imp_arrow:
                print('error: invalid formula, expected implication arrow due to -')
                return False
            elif open_brac['<']:
                active_program = False
                bimp_arrow = True
                open_brac[x] = False
                # undo the extend and append activated by '<'
                stack.pop()
                stack = [[stack[0][0]]]
            else:
                imp_arrow = True
        elif x == '<' or x == '[':
            open_brac[x] = True
            active_program = True
            stack[-1].extend([x,[]])
            stack.append(stack[-1][-1])
        elif x == '>' or x == ']':
            if imp_arrow and x == '>':
                stack[-1].append('->')
                imp_arrow = False
            elif bimp_arrow and x == '>':
                stack[-1].append('<->')
                bimp_arrow = False
            else:
                stack.pop()
                if len(stack[-1][-1]) > 3:
                    print('error: to many arguments between parentheses')
                    return False
                if not open_brac[close_brac[x]]:
                    print('error: misaligned program brackets')
                    return False
                open_brac[close_brac[x]] = False
                active_program = False
        elif x == '+' or x == '*' or x == '?' or x == '^':
            stack[-1][-1] = [x, stack[-1][-1]]
        elif x == '(':
            if negation:
                negation = False
                stack[-1].append(['~',[]])
                stack.append(stack[-1][-1][-1])
            else:
                stack[-1].append([])
                stack.append(stack[-1][-1])
        elif x == ')':
            stack.pop()
            if not stack:
                print('error: opening bracket is missing')
                return False
            if len(stack[-1][-1]) > 3:
                print('error: to many arguments between parentheses')
                return False
        else:
            if negation:
                stack[-1].append(['~', x])
                negation = False
            else:
                stack[-1].append(x)
    if len(stack) > 1:
        print('error: closing bracket is missing')
        return False
    if len(stack[0]) > 3:
        print('error: too many arguments between parentheses')
        return False
    return stack.pop()



"""
while True:
    c = PDLparser(['p','q','r','s'],['a','b','c','d'])
    # ~(p&q) Or (~p & ~q)
    s = input("Enter a logical formula: ")
    #ret = c.parse_rec(s)
    ret = c.parse(s)
    print(ret)
"""
