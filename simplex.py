import sys
import copy
import numpy as np
from fractions import Fraction

def make_dictionary():        #should read from stdin and return a dictionary for the input LP
#----------------------------------#
# should read from stdin and return a dictionary for the input LP
# Will have Fractions as entries
#----------------------------------#
    #dictionary = [                #a setup dictionary [constants, x1, x2, w1, w2, w3] *for a 2 opt var, 3 constraint problem
    #    [Fraction(0),Fraction(3),Fraction(-3),Fraction(-2),Fraction(0),Fraction(0)],
    #    [Fraction(4),Fraction(-2),Fraction(2),Fraction(1),Fraction(1),Fraction(0)],
    #    [Fraction(-5),Fraction(1),Fraction(-1),Fraction(3),Fraction(0),Fraction(1)]
    #]

    dictionary = [
        [0,3,-3,-2,0,0],
        [4,-2,2,1,1,0],
        [-5,1,-1,3,0,1]
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
    
    leaving_basis_var_col = -1                                  #<----pivot_col is the col of the leaving var
    for col, var in enumerate(basis):               #<----- UPDATE THE BASIS: sub in omega and out the old basis var
        if var == 1:                                #<----should always be one
            if auxillary[least_feasible_row][col] == 1:     #<------means this is the basis var in the equation as all other basis vars must be 0 (a basis var cannot be expressed in terms of other basis var)
                basis[col] = 0
                basis[-1] = 1
                leaving_basis_var_col = col
                break
    
    #---------------pivot in omega for least feasible constraint---------------#
    auxillary[least_feasible_row] = np.array(auxillary[least_feasible_row]) / -1        #<---- DO PIVOT IN PIVOT ROW (will work with fractions)
    auxillary[least_feasible_row][leaving_basis_var_col] = 1                                        #<---- set old basis_var to 1 snce math messed up and made it -1
    auxillary[least_feasible_row][-1] = 1                                               #<---- set omega to 1 math made it -1 aswell
    
    #-------------substitute into rest of constraints--------------------------#
    # pivot_col is the entering var, will always be omega thus pivot_col = -1(last col)
    #--------------------------------------------------------------------------#
    
    for eq_i, eq in enumerate(auxillary):
        if eq_i != least_feasible_row:
            factor = np.array(auxillary[least_feasible_row]) * auxillary[eq_i][-1]
            auxillary[eq_i] = np.array(auxillary[eq_i]) + factor                
            auxillary[eq_i][-1] = 0                                      #<------ set basic var to 0 in eqn that dont involve it

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

def do_pivot(dictionary, basis, pivot_col, pivot_row):
    #------------------------------------------------#
    # Will make this work with only numpy arrays, aux problems are already arrays
    #initially feasible probs will have ot be converte to numpy arrays befor calling do_pivot
    #------------------------------------------------#

    #--------pivot in entering val in our tightest constraint---#
    factor = dictionary[pivot_row][pivot_col]
    rescaling_arr = [None] * len(dictionary[pivot_row])                                          #<- for dividing the numpy array at pivot row by the correct factors
    rescaling_arr = np.array(rescaling_arr)

    for i in range(len(dictionary[pivot_row])):                 #<- create rescaling_arr with the appropriate factors based on entering var having negative coefficient
        if basis[i] == 1 and dictionary[pivot_row][i] == 1:     #<- if we are the old basis var flip sign
            rescaling_arr[i] = factor
            old_basis_col = i
        elif i == pivot_col:                                    #<- if we are the entering var flip sign (the math messes this up)
            rescaling_arr[i] = factor
        else:
            rescaling_arr[i] = -1*factor

    dictionary[pivot_row] = np.divide(dictionary[pivot_row], rescaling_arr)
    print(dictionary)
    
    #-------update rest of constraints--------------------------------#
    for eq_i, eq in enumerate(dictionary):
        if eq_i != pivot_row:
            factor = np.array(dictionary[pivot_row]) * dictionary[eq_i][pivot_col]
            dictionary[eq_i] = np.array(dictionary[eq_i]) + factor                
            dictionary[eq_i][pivot_col] = 0 

    #------update basis---------------------------------#
    for i in range(len(basis)):
        if i == pivot_col:
            basis[i] = 1
        elif i == old_basis_col:
            basis[i] = 0

    return(dictionary, basis)

def solve(dictionary, basis):
    #-watchout for unboundedness
    #-watch for cycling 
    #-watch aux problem is a list of "numpy arrays" might cause problems

    method = "Largest_coeff"

    while not_optimal(dictionary):
        prev_obj_val = dictionary[0][0]
        pivot_col, pivot_row, unbounded  = get_pivot(dictionary, basis, method)
        #---------TODO-----------#
        # if unbounded is true need to deal with that probably end function here
        if unbounded == True:
            print("UNBOUNDED")
            exit()
        #------------------------#
        dictionary = do_pivot(dictionary, basis, pivot_col, pivot_row)

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
    basis = [0,0,0,0,1,1]      #for [const,x1,x2,w1,w2,w3] where w1,w2,w3 in basis

    prev_obj_val = dictionary[0][0]
    #----------------------------

    #----------------------------
    #Check if initital dictionary feasible
    #solve aux problem if not
    if not_feasible(dictionary):
        auxillary, basis = create_aux_problem(dictionary, basis)
        
        pivot_col, pivot_row, unbounded = get_pivot(auxillary, basis, "Largest_coeff")
        auxillary, basis = do_pivot(auxillary, basis, pivot_col, pivot_row)
        
        #auxillary = solve(auxillary, basis)
        #solution = get_solution(auxillary)
        #if optimal_obj_val != 0:
        #    infeasible
    #----------------------------
    #print(dictionary)
    #print(basis)
    #pivot_col, pivot_row, unbounded = get_pivot(dictionary, basis, "Largest_coeff")
    #print(pivot_col)
    #print(pivot_row)
    #dictionary, basis = do_pivot(dictionary, basis, pivot_col, pivot_row)
    #print(dictionary)
    #print(basis)

    print('hi')

    


if __name__ == "__main__":
    main()
