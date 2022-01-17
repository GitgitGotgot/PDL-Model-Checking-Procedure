import timeit
# import stopwatch
import sys
import PropParser as parse
import ModelGen as gen
from MCP import Kripke

def main(argv):
    RunTests = False
    sparse=False
    if len(argv) < 3:
        raise Exception("Please enter the model you want to check:\n"
                        "To generate a model via text file enter: python main.py --file \"file_name.txt\"\n"
                        "To run the given tests in a text file enter: python main.py --file \"file_name.txt\" --T\n"
                        "To generate a random model enter: python main.py --random \"model_size\"\n"
                        "To generate a model that forms a straight line enter: python main.py --line \"model_size\" \"p_loc\"\n"
                        "To generate a model that forms a circle enter: python main.py --circle \"model_size^2\" \"p_loc\"\n"
                        "To generate a model that forms a rectangular grid enter: python main.py --grid \"model_size\" \"p_loc\"\n"
                        "Input for model size or p_loc will set to default (50 and 0 respectively) if they're not a positive integer\n"
                        "For sparse matrix structures add --sparse at the end of the command line\n"
                        )
        exit(-1)
    if argv[-1] == '--sparse':
        sparse=True

    if argv[1] == "--file":
        try:
            f = open(argv[2])
            f.close()
        except FileNotFoundError:
            print('File does not exist or wrong input')
        N, State_V, Adj_M, Tests = gen.ModelFromFile(argv[2], sparse_matrix=sparse)
        if len(argv) > 3:
            if argv[3] == "--T":
                RunTests = True

    elif argv[1] == "--random":
        # N = int(argv[2]) if (int(argv[2]) > 0) else 50
        N = int(argv[2]) if (argv[2].isdigit()) and (int(argv[2]) > 0) else 50
        State_V, Adj_M = gen.RandomModel(N, sparse_matrix=sparse)

    elif argv[1] == "--line":
        N = int(argv[2]) if (argv[2].isdigit()) and (int(argv[2]) > 0) else 50
        if len(argv) > 3:
            p_loc = int(argv[3]) if (argv[3].isdigit()) and (int(argv[3]) < N) and (int(argv[3]) > 0) else False
        else:
            p_loc = False
        State_V, Adj_M = gen.LineModel(N, p_loc, sparse_matrix=sparse)

    elif argv[1] == "--circle":
        N = int(argv[2]) if (argv[2].isdigit()) and (int(argv[2]) > 0) else 50
        if len(argv) > 3:
            p_loc = int(argv[3]) if (argv[3].isdigit()) and (int(argv[3]) < N) and (int(argv[3]) > 0) else False
        else:
            p_loc = False
        State_V, Adj_M = gen.CircleModel(N, p_loc, sparse_matrix=sparse)

    elif argv[1] == "--grid":
        N = int(argv[2]) if (argv[2].isdigit()) and (int(argv[2]) > 0) else 50
        if len(argv) > 3:
            p_loc = int(argv[3]) if (argv[3].isdigit()) and (int(argv[3]) < N) and (int(argv[3]) > 0) else False
        else:
            p_loc = False
        State_V, Adj_M = gen.GridModel(N, p_loc, sparse_matrix=sparse)

    elif argv[1] =="--h":
        print("Please enter the model you want to check:\n"
              "To generate a model via text file enter: python main.py --file \"file_name.txt\"\n"
              "To run the given tests in a text file enter: python main.py --file \"file_name.txt\" --T\n"
              "To generate a random model enter: python main.py --random \"model_size\"\n"
              "To generate a model that forms a straight line enter: python main.py --line \"model_size\" \"p_loc\"\n"
              "To generate a model that forms a circle enter: python main.py --circle \"model_size\" \"p_loc\"\n"
              "To generate a model that forms a rectangular grid enter: python main.py --grid \"model_size\" \"p_loc\"\n\n"
              "Input for model size or p_loc will set to default (50 and 0 respectively) if they're not a positive integer\n"
              "For sparse matrix structures add --sparse at the end of the command line\n"
              )
    # Generate the model
    k = Kripke(Adj_M, State_V, N)

    StdTests = ['([a*]p)->([a;(a;(a;(a;a)))]p)', '(!([a]p))->(!([aUb]p))']

    # Run tests from file
    if RunTests:
        if len(Tests) == 0:
            print('Model has no available tests')
        else:
            for t in Tests:
                formula = parse.FormulaParser(t, State_V.keys(), list(Adj_M.keys()).remove('IDENTITY'))
                if not formula:
                    print("Invalid formula in Tests.")
                else:
                    print("Test:" + str(t))
                    print('Result:' + str(k.MCP(formula)))
                    t = timeit.timeit(lambda:'k.MCP(formula)')
                    print('Time:' + str(t))
    else:
        while True:
            s = input("Enter a PDL formula: ")
            if s == 'h':
                print("Compound formulas and programs must always be between parentheses\n"
                      "EXAMPLE: <a;(bUc)>(p->q)\n\n"
                      "Formula Operators:\n"
                      "<a>p = <a>p\n"
                      "[a]p = [a]p\n"
                      "Loop(a) = L(a)\n"
                      "Repeat(a) = R(a)\n"
                      "Negation(p) = !p\n"
                      "Logical AND = &\n"
                      "Logical OR = /\n"
                      "Implication = ->\n\n"
                      "Program Operators:\n"
                      "Complement(a) = !a\n"
                      "Test(p) = (p)?\n"
                      "Converse(p) = (p)'\n"
                      "Kleene_Plus(a) = a+\n"
                      "Kleene_Star(a) = a*\n"
                      "Composition = ;\n"
                      "Union = U\n"
                      "Intersection = X\n\n"
                      "To run all tests, insert 't' "
                      )
            elif s=='t':
                for t in StdTests:
                    print("Test:" + str(t))
                    formula = parse.FormulaParser(t, State_V.keys(), list(Adj_M.keys()).remove('IDENTITY'))
                    print('Result:' + str(k.MCP(formula)))
                    t = timeit.timeit(lambda:'k.MCP(formula)')
                    print('Time:' + str(t))
            else:
                formula = parse.FormulaParser(s, State_V.keys(), list(Adj_M.keys()).remove('IDENTITY'))
                if not formula:
                    print("Press h for help.")
                else:
                    print(k.MCP(formula))
        #              )
if __name__ == '__main__':
    main(sys.argv)
