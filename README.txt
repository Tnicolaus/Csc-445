README.txt
Tristan Nicolaus, V00913393

My code runs exactly as described in the project outline. With a file piped in, and no extra command line arguments.

Description of Architecture:
    I implemented a basic simplex algorithm that can use either the largest coefficient rule or the largest increase rule to select which pivot to perform. 
    Currently it uses largest increase as the default, but I left the code in for largest increase for you to examine if you would like. 
    Initially infeasible problems are resolved through auxillary method. If the initial LP is infeasible, I create an auxillary problem by calling create_aux_problem()
    and then solve it with solve_aux(), which is exactly like solve() but watches for omega in the basis when the dictionary is optimal. when the auxiliary
    problem is solved if its optimal value is not zero my program outputs infeasible. 
    If it is feasible we recreate the feasible original dictionary from the solved auxiliary problem with
    reintroduce(), and then solve that through the simplex method by calling solve(). The solver watches for unboundedness at each get_pivot() step, 
    where it is selecting the next pivot. If it detects an unbounded col in the dictionary(all positive entries) it outputs unbounded and exits.

    Solving the dictionary consists of calling solve() which in turn calls get_pivot() and do_pivot(), until the dictionary is optimal. each call to solve
    decides the pivot selection stratedgy for the next iteration. When the dictionary is optimal we output the coresponding values.

    get_pivot() iterates over the entries in the obj function and decides which is the best entering var based upon the pivot scheme, and then iterates over the
    rows of the dictionary to pick the tightest constraint and thus the leaving variable(again depending on pivot selection scheme, if its largest increase get pivot 
    iterates over all possible entering variables and corresponding leaving variables to pick the best one as described below).

    do_pivot() takes the entering variable(pivot_col) and the leaving variable(pivot_row) and performs the pivot inplace in our dictionary by first pivoting the pivot_row
    and then calculating all of the other rows(slack equations) after subbing in the new basis variable. It then returns this new dictionary.

    create_aux_problem() takes the original infeasible dictionary, adds a col for omega, and zeros out the objective equation row. It then adds a -1 in the objective
    equation row in the omega col and a 1 in all the other rows omega cols. After this it subs in omega for the least feasible constraint to create a feasble dictionary
    which it returns.

    get_obj_increase() is explained in the EXTRA part

    reintroduce() is pretty straight forward and just reintroduces the orginal objective equation into the new dictionary simillar to completing a pivot

    Make_dictionary() reads input from stdin and converts it to a 2D numpy array corresponding to the dictionary that problem would have. each row is an equation 
    in the dictionary

    not_feasible(), not_optimal(), get_obj_val(), get_optimal_point() are very straightforward

    EXTRA: "Largest coefficient"
    if the pivot selection method is largest increase, in get_pivot(); my program creates a biggest increase variable to keep track of the best pivot so far in terms of increase
    to the obj function. Then it iterates over all possible entering variables in the obj function, and for each of those picks the leaving variable with the tightest 
    constraint. Then get_pivot() calls get_obj_increase() which does the pivot in a copy of the corresponding row from the actual dictionary and substitutes this into a copy of the objective
    function to compute the increase in objective value this pivot would have. We then return the pivot that provides the greatest increase, and in the case of a tie
    it returns the pivot with the lowest index entering variable.

    This solver recognizes possible cycling through a pivot that doesnt increase the objective functions value. If this is encountered it falls back on blands until 
    the objective value increases and then reverts back to largest increase(or largest coefficient) for our pivot selection rule. 
