import sys
import copy
import numpy as np
from fractions import Fraction

def make_dictionary():        #should read from stdin and return a dictionary for the input LP
    dictionary = [                #a setup dictionary [constants, x1, x2, w1, w2, w3] *for a 2 opt var, 3 constraint problem
        [0,1,1,0,0,0],      #starts out w1, w2, w3 in basis
        [-2,1,-1,1,0,0],
        [4,-1,0,0,1,0],
        [4,0,-1,0,0,1]
    ]
    return dictionary

def not_feasible(dictionary):
    for i in range(1, len(dictionary)):
        if dictionary[i][0] < 0:
            return True

    return False

def create_aux_problem(dictionary, basis):
    auxillary = copy.deepcopy(dictionary)           #<-----might be bad for performance
    for row in range(len(auxillary)):
        if row == 0:
            for entry in range(len(auxillary[row])):               #<--- zero out first row
                auxillary[row][entry] = 0
            auxillary[row] = auxillary[row] + [-1]                #<--- add negative omega col
        else:
            auxillary[row] = auxillary[row] + [1]
    basis = basis + [0]                            #<------add omega into basis vector as 0 since not in basis yet
    
    #-------------------------------------------
    #pivot in omega for least feasible constraint
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

    auxillary[least_feasible_row] = np.array(auxillary[least_feasible_row]) / -1        #<---- DO PIVOT IN PIVOT ROW (will work with fractions)
    auxillary[least_feasible_row][pivot_col] = 1                                        #<---- set new basis variable to 1
    
    
    for eq_i, eq in enumerate(auxillary):
        if eq_i != least_feasible_row:
            multiplier = np.array(auxillary[least_feasible_row]) * auxillary[eq_i][pivot_col]
            auxillary[eq_i] = np.array(auxillary[eq_i]) + multiplier                
            auxillary[eq_i][pivot_col] = 0                                      #<------ set basic var to 0 in eqn that dont involve it
    
    return auxillary, basis

def main():
    # -------TODO----------------
    # make our initial dictionary
    dictionary = make_dictionary()
    #--------TODO----------------
    #construct a list of which vectors are in the basis
    basis = [0,0,0,1,1,1]      #for [const,x1,x2,w1,w2,w3] where w1,w2,w3 in basis

    prev_obj_val = dictionary[0][0]
    method = 'largest_coeff'
    #----------------------------

    #----------------------------
    #Check if initital dictionary feasible
    #solve aux problem if not
    if not_feasible(dictionary):
        auxillary = create_aux_problem(dictionary, basis)
        
        #auxillary = solve(auxillary)
        #solution = get_solution(auxillary)
        #if optimal_obj_val != 0:
        #    infeasible
    #----------------------------
    print('hi')

    #while not_optimal(dictionary):
    #    entering_var = get_entering_var(dictionary)


if __name__ == "__main__":
    main()
