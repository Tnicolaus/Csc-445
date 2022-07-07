import sys
import copy
import numpy as np
from fractions import Fraction

def make_dictionary():        #should read from stdin and return a dictionary for the input LP
    dictionary = [                #a setup dictionary [constants, x1, x2, w1, w2, w3] *for a 2 opt var, 3 constraint problem
        [0,2,1,0,0,0,0,0],      #starts out w1, w2, w3 in basis
        [-3,1,1,1,0,0,0,0],
        [-1,1,0,0,1,0,0,0],
        [4,-1,0,0,0,1,0,0],
        [-1,0,1,0,0,0,1,0],
        [20,-3,-4,0,0,0,0,1]
    ]
    return dictionary

def not_feasible(dictionary):
    for i in range(1, len(dictionary)):
        if dictionary[i][0] < 0:
            return True

    return False

def create_aux_problem(dictionary, basis):
    #------------------------------------#
    # takes an infeasible dictionary and 
    # returns the feasible dictionary after
    # Omega has been put in the basis
    # along with the new basis
    #------------------------------------#

    #--create dictionary with omega------#
    auxillary = copy.deepcopy(dictionary)           #<-----might be bad for performance
    for row in range(len(auxillary)):
        if row == 0:
            for entry in range(len(auxillary[row])):               #<--- zero out first row
                auxillary[row][entry] = 0
            auxillary[row] = auxillary[row] + [-1]                #<--- add negative omega col
        else:
            auxillary[row] = auxillary[row] + [1]
    basis = basis + [0]                            #<------add omega into basis vector as 0 since not in basis yet
    
    #---Find least feasible constraint---------#
    min = 0
    least_feasible_row = -1                     #<------FIND LEAST FEASIBLE CONSTRAINT TO SWAP FOR OMEGA
    for i, row in enumerate(auxillary):
        if row[0] < min:
            min = row[0]
            least_feasible_row = i
    
    if least_feasible_row == -1:
        print("aux problem error")
        exit()

    exit_var = -1
    pivot_col = -1
    for col, var in enumerate(basis):               #<----- UPDATE THE BASIS: sub in omega and out the old basis var
        if var == 1:                                #<----should always be one
            if auxillary[least_feasible_row][col] == 1:     #<------means this is the basis var in the equation as all other basis vars must be 0 (a basis var cannot be expressed in terms of other basis var)
                basis[col] = 0
                basis[-1] = 1
                pivot_col = col
   
    #---------------pivot in omega for least feasible constraint---------------#
    auxillary[least_feasible_row] = np.array(auxillary[least_feasible_row]) / -1        #<---- DO PIVOT IN PIVOT ROW (will work with fractions)
    auxillary[least_feasible_row][pivot_col] = 1                                        #<---- set new basis variable to 1
    
    
    for eq_i, eq in enumerate(auxillary):
        if eq_i != least_feasible_row:
            multiplier = np.array(auxillary[least_feasible_row]) * auxillary[eq_i][pivot_col]
            auxillary[eq_i] = np.array(auxillary[eq_i]) + multiplier                
            auxillary[eq_i][pivot_col] = 0                                      #<------ set basic var to 0 in eqn that dont involve it
    
    return auxillary, basis

def not_optimal(dictionary):
    for i, val in enumerate(dictionary[0]):
        if i > 0 and val > 0:
            return True

    return False

def get_pivot(dictionary, basis, method):
    #-----------------------------------#
    # returns a pivot_col(entering var)
    # a pivot_row(leaving var) and weather
    # or not the problem in unbounded
    #-----------------------------------#

    max = -1
    pivot_col = -1
    unbounded = False
    pivot_row = None
    min_limiting_val = None

    if method == "Largest_coeff":
        #-----get pivot_col -> entering variable-----#
        for i, val in enumerate(dictionary[0]):
            if i > 0 and val > max:
                pivot_col = i
                max = val

        #-----get pivot_row -> leaving variable----------------------------------#
        for i in range(1, len(dictionary)):
            eq = dictionary[i]
            if eq[pivot_col] < 0:
                cur_limiting_val = abs(eq[0] / eq[pivot_col])                     #<--- check restriction imposed by entering var in this eqn
                if min_limiting_val == None or cur_limiting_val < min_limiting_val:      #<- it is a bound and (no bound is set or its a min bound)
                    min_limiting_val = cur_limiting_val
                    pivot_row = i

    elif method == "Blands":
        #----choose smallest index var not in basis to enter and smallest index var in basis w negative coeff on the entering var to leave-----#
        #-------get pivot_col -> entering var--------#
        for i in range(1, len(basis)):
            if basis[i] == 0 and dictionary[0][i] > 0:
                pivot_col = i
                break

        #-------get pivot_row -> leaving var-------------#
        #scan through basis for lowest index vaiable
        #find eq for that variable and check if it has -coeff on entering pivot_col
        done = 0
        for i in range(1, len(basis)):
            if basis[i] == 1 and done == 0:
                for eq in range(1, len(dictionary)):                 #<--- skip obj function row in basis
                    if dictionary[eq][i] == 1:
                        if dictionary[eq][pivot_col] < 0:
                            pivot_row = eq
                            done = 1
                            break

    #--------check for unboundedness------#
    if pivot_row == None:
        unbounded = True
            
    return pivot_col, pivot_row, unbounded


def solve(dictionary, basis):
    #-watchout for unboundedness
    #-watch for cycling 
    #-watch aux problem is a list of "numpy arrays" might cause problems

    method = "Largest_coeff"

    while not_optimal(dictionary):
        #prev_obj_val = dictionary[0][0]
        #pivot_col, pivot_row, unbounded  = get_pivot(dictionary, basis, method)
        #---------TODO-----------#
        # if unbounded is true need to deal with that probably end function here
        #------------------------#
        #dictionary = do_pivot(dictionary, basis, pivot_col, pivot_row)
        new_obj_val = dictionary[0][0]
        if new_obj_val == prev_obj_val:                                 #<---- if obj val remains constant -> degeneracy -> could be cycling, use blands to avoid
            method = "Blands"
        else:
            method = "Largest_coeff"

    return dictionary, basis


def main():
    # -------TODO----------------
    # make our initial dictionary
    dictionary = make_dictionary()
    #--------TODO----------------
    #construct a list of which vectors are in the basis
    basis = [0,0,0,1,1,1,1,1]      #for [const,x1,x2,w1,w2,w3] where w1,w2,w3 in basis

    prev_obj_val = dictionary[0][0]
    #----------------------------

    #----------------------------
    #Check if initital dictionary feasible
    #solve aux problem if not
    if not_feasible(dictionary):
        auxillary, basis = create_aux_problem(dictionary, basis)
        print(auxillary)
        print(basis)
        pivot_col, pivot_row, unbounded = get_pivot(auxillary, basis, "Largest_coeff")
        print(pivot_col)
        print(pivot_row)
        print(unbounded)
        #auxillary = solve(auxillary, basis)
        #solution = get_solution(auxillary)
        #if optimal_obj_val != 0:
        #    infeasible
    #----------------------------

    print('hi')

    


if __name__ == "__main__":
    main()
