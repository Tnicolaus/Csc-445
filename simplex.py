import sys
import copy
import numpy as np
from fractions import Fraction

def make_dictionary():        #should read from stdin and return a dictionary for the input LP
#----------------------------------#
# should read from stdin and return a 2D array for the input LP
# Will have Fractions as entries
#----------------------------------#
# - iterate over lines in file ignore whitespace lines
# - keep count of lines for number of slack vars
# - put each line into a 2D list, re order entrys appropriately, first is different
# - add zeros padding the end of each list for number of slack vars and ones for correct eqn
    slack_vars = -1                         #<- first row is obj eq
    dictionary = []

    #------put each line into a list then into dictionary------#
    for line in sys.stdin:                  
        if not line.isspace():              
            line = line.strip().split()
            for i in range(len(line)):
                line[i] = Fraction(line[i])
            slack_vars += 1
            if slack_vars == 0:             #<- if obj eq         
                line = [Fraction(0)] + line           #<- add zero to first col of obj eq 
            dictionary.append(line)

    #------re-order the constraint lines so they are slack eq and zero pad each row and add basis 1-----#
    for row in range(len(dictionary)):
        if row != 0:
            #reorder inplace
            slack_val = dictionary[row][-1]
            for i in range(len(dictionary[row])-1, 0 , -1):
               dictionary[row][i] = -1 * dictionary[row][i-1]
            dictionary[row][0] = slack_val
    
            for i in range(1, slack_vars+1):
                if row != i:
                    dictionary[row].append(Fraction(0))
                else:
                    dictionary[row].append(Fraction(1))

        else:
            for i in range(slack_vars):
                dictionary[row].append(Fraction(0))

    dictionary = np.array(dictionary)

    #-----make basis-------------------------------#
    basis = []
    dim = len(dictionary[0])
    for i in range(dim):
        if i < dim - slack_vars:
            basis.append(0)
        else:
            basis.append(1)

    print(dictionary)
    print()
    print(basis)
    print()


#-----example 5 simplex examples 2-----#
# worked until optimal 
    #dictionary = np.array([
    #    [Fraction(0),Fraction(-2),Fraction(-1),Fraction(0),Fraction(0),Fraction(0)],
    #    [Fraction(-1),Fraction(1),Fraction(-1),Fraction(1),Fraction(0),Fraction(0)],
    #    [Fraction(-2),Fraction(1),Fraction(2),Fraction(0),Fraction(1),Fraction(0)],
    #    [Fraction(1),Fraction(0),Fraction(-1),Fraction(0),Fraction(0),Fraction(1)]
    #])
    #basis = [0,0,0,1,1,1]

#-----example 1 simplex examples 2-----#
# worked got unbounded
    #dictionary = np.array([
    #    [Fraction(0),Fraction(1),Fraction(0),Fraction(0),Fraction(0)],
    #    [Fraction(1),Fraction(-1),Fraction(1),Fraction(1),Fraction(0)],
    #    [Fraction(2),Fraction(1),Fraction(-1),Fraction(0),Fraction(1)]
    #])
    #basis = [0,0,0,1,1]

#-----example 3 simplex examples 2-----#
#worked got optimal dictionary
    #dictionary = np.array([
    #    [Fraction(0),Fraction(1),Fraction(2),Fraction(3),Fraction(0),Fraction(0)],
    #    [Fraction(3),Fraction(-1),Fraction(0),Fraction(-1),Fraction(1),Fraction(0)],
    #    [Fraction(2),Fraction(0),Fraction(-1),Fraction(-2),Fraction(0),Fraction(1)]
    #])
    #basis = [0,0,0,0,1,1]

#----ex degenerate pivots(2) lecture 8--------#
#Worked with blands got optimal dictionary
    #dictionary = np.array([
    #    [Fraction(0), Fraction(1), Fraction(1), Fraction(1), Fraction(0), Fraction(0), Fraction(0)],
    #    [Fraction(2), Fraction(-1), Fraction(-1), Fraction(0), Fraction(1), Fraction(0), Fraction(0)],
    #    [Fraction(2), Fraction(-1), Fraction(0), Fraction(-1), Fraction(0), Fraction(1), Fraction(0)],
    #    [Fraction(2), Fraction(0), Fraction(-1), Fraction(-1), Fraction(0), Fraction(0), Fraction(1)]
    #])
    #basis = [0,0,0,0,1,1,1]

#---ex cycling(2) lecture 8----------#
#worked got optimal 1.25
    #dictionary = np.array([
    #    [Fraction(0), Fraction(3,4), Fraction(-20), Fraction(1,2), Fraction(-6), Fraction(0), Fraction(0), Fraction(0)],
    #    [Fraction(0), Fraction(-1,4), Fraction(8), Fraction(1), Fraction(-9), Fraction(1), Fraction(0), Fraction(0)],
    #    [Fraction(0), Fraction(-1,2), Fraction(12), Fraction(1,2), Fraction(-3), Fraction(0), Fraction(1), Fraction(0)],
    #    [Fraction(1), Fraction(0), Fraction(0), Fraction(-1), Fraction(0), Fraction(0), Fraction(0), Fraction(1)]
    #])
    #basis = [0,0,0,0,0,1,1,1]

#---ex 1 simplex examples 1----------#
#worked got optimal 17
    #dictionary = np.array([
    #    [Fraction(0), Fraction(8), Fraction(4), Fraction(2), Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
    #    [Fraction(8), Fraction(-2), Fraction(-4), Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(0)],
    #    [Fraction(4), Fraction(-1), Fraction(-1), Fraction(-1), Fraction(0), Fraction(1), Fraction(0), Fraction(0)],
    #    [Fraction(1), Fraction(-1), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(1), Fraction(0)],
    #    [Fraction(1), Fraction(0), Fraction(-1), Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(1)]
    #])
    #basis = [0,0,0,0,1,1,1,1,]

#------vanderbei_exercise2.10.txt----------------#

    #dictionary = np.array([
    #    [Fraction(0), Fraction(6), Fraction(8), Fraction(5), Fraction(9), Fraction(0), Fraction(0)],
    #    [Fraction(1), Fraction(-1), Fraction(-1), Fraction(-1), Fraction(-1), Fraction(1), Fraction(0)],
    #    [Fraction(-1), Fraction(1), Fraction(1), Fraction(1), Fraction(1), Fraction(0), Fraction(1)]
    #])
    #basis = [0,0,0,0,0,1,1]

#-----vanderbei_exercise2.6.txt-----------------#
    #dictionary = np.array([
    #    [Fraction(0), Fraction(1), Fraction(3), Fraction(0), Fraction(0), Fraction(0)],
    #    [Fraction(-3), Fraction(1), Fraction(1), Fraction(1), Fraction(0), Fraction(0)],
    #    [Fraction(-1), Fraction(1), Fraction(-1), Fraction(0), Fraction(1), Fraction(0)],
    #    [Fraction(2), Fraction(-1), Fraction(-2), Fraction(0), Fraction(0), Fraction(1)]
    #])
    #basis = [0,0,0,1,1,1]

    return dictionary, basis

def not_feasible(dictionary):
    for i in range(1, len(dictionary)):
        if dictionary[i, 0] < 0:
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
    auxillary = dictionary
    auxillary[0] = np.array([Fraction(0) for i in auxillary[0]])
    new_col = [[Fraction(1)] for i in range(len(auxillary))]
    new_col[0] = [Fraction(-1)]
    auxillary = np.append(auxillary, new_col, axis=1)
    
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
    

    leaving_basis_var_col = -1                                  
    for col, var in enumerate(basis):               #<----- UPDATE THE BASIS: sub in omega and out the old basis var
        if var == 1:                                #<----should always be one
            if auxillary[least_feasible_row][col] == 1:     #<------means this is the basis var in the equation as all other basis vars must be 0 (a basis var cannot be expressed in terms of other basis var)
                basis[col] = 0
                basis[-1] = 1
                leaving_basis_var_col = col
                break
   
    #---------------pivot in omega for least feasible constraint---------------#
    #auxillary[least_feasible_row] = np.array(auxillary[least_feasible_row]) / -1        #<---- DO PIVOT IN PIVOT ROW (will work with fractions)
    auxillary[least_feasible_row] = auxillary[least_feasible_row] / -1        #<---- DO PIVOT IN PIVOT ROW (will work with fractions)
    auxillary[least_feasible_row][leaving_basis_var_col] = Fraction(1)                                        #<---- set old basis_var to 1 snce math messed up and made it -1
    auxillary[least_feasible_row][-1] = Fraction(1)                                               #<---- set omega to 1 math made it -1 aswell
    
    #-------------substitute into rest of constraints--------------------------#
    # pivot_col is the entering var, will always be omega thus pivot_col = -1(last col)
    #--------------------------------------------------------------------------#
    
    for eq_i, eq in enumerate(auxillary):
        if eq_i != least_feasible_row:
            factor = auxillary[least_feasible_row] * auxillary[eq_i][-1]
            auxillary[eq_i] = auxillary[eq_i] + factor                

            auxillary[eq_i][-1] = Fraction(0)                                      #<------ set basic var to 0 in eqn that dont involve it

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
        #----choose smallest index var not in basis w positive coeff to enter and var in basis w tightest bound to leave if tie choose lowest number-----#
        #-------get pivot_col -> entering var--------#
        for i in range(1, len(basis)):
            if basis[i] == 0 and dictionary[0][i] > 0:
                pivot_col = i
                break

        #-------get pivot_row -> leaving var-------------#
        #scan through basis for lowest index vaiable
        #find eq for that variable and check if it has tighter bound then current variable row and has negative entry for entering var
        cur_ratio = -1
        for i in range(1, len(basis)):
            if basis[i] == 1:
                for eq in range(1, len(dictionary)):                                                         #<--- skip obj function row in basis
                    if dictionary[eq][i] == 1 and dictionary[eq][pivot_col] < 0:                             #<-correct row and row has neg coeff on entering var
                        ratio = abs(dictionary[eq][0] / dictionary[eq][pivot_col])
                        if ratio < cur_ratio or cur_ratio == -1 :  #<-tightest bound
                            pivot_row = eq
                            cur_ratio = ratio
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


    #-------update rest of constraints--------------------------------#
    for eq_i, eq in enumerate(dictionary):
        if eq_i != pivot_row:
            factor = dictionary[pivot_row] * dictionary[eq_i][pivot_col]
            dictionary[eq_i] = np.array(dictionary[eq_i]) + factor                
            dictionary[eq_i][pivot_col] = Fraction(0) 

    #------update basis---------------------------------#
    for i in range(len(basis)):
        if i == pivot_col:
            basis[i] = 1
        elif i == old_basis_col:
            basis[i] = 0
    
    return(dictionary, basis)

def get_obj_val(dictionary):
    return dictionary[0][0]

def solve(dictionary, basis, method):
    #-watchout for unboundedness
    #-watch for cycling 
    #-All dictionaries are a list of "numpy arrays" 

    while not_optimal(dictionary):
        prev_obj_val = dictionary[0][0]
        pivot_col, pivot_row, unbounded  = get_pivot(dictionary, basis, method)

        #print(method)
        #print(pivot_col)
        #print(pivot_row)
        #---------TODO-----------#
        # if unbounded is true need to deal with that probably end function here
        if unbounded == True:
            print("unbounded")
            exit()
        #------------------------#
        dictionary, basis = do_pivot(dictionary, basis, pivot_col, pivot_row)

        #print(dictionary)
        #print()

        new_obj_val = dictionary[0][0]
        if new_obj_val == prev_obj_val:                                 #<---- if obj val remains constant -> degeneracy -> could be cycling, use blands to avoid
            method = "Blands"
        else:
            method = "Largest_coeff"

    return dictionary, basis

def reintroduce(dictionary, basis, obj_eq):
    #------plan-------#
    # -Obj_eq is an array
    # -iterate over obj_function
    # - if var in basis, create new array with coeff of var(factor) * row for var(eqn)
    #        - first turn entry of var to 0 in eqn then multiply as its not in new obj function
    #        - zero out var in obj function as its already been counted
    # - add together obj function and all of these vectors for new obj function
    sum = np.array([Fraction(0) for i in obj_eq])

    for col in range(len(obj_eq)):
        if basis[col] == 1 and obj_eq[col] != 0:                     #<- If var in basis and in obj function
            coeff_of_var = obj_eq[col]
            obj_eq[col] = Fraction(0)                                #<- zero out subed in var in obj function
            for row in range(1,len(dictionary)):
                if dictionary[row][col] == 1:
                    eqn_for_var = copy.deepcopy(dictionary[row])
                    eqn_for_var[col] = Fraction(0)                   #<- zero out subed in var in constraint eqn
                    break
            sum = sum + (eqn_for_var * coeff_of_var)

    new_obj_eq = sum + obj_eq
    dictionary[0] = new_obj_eq

    return dictionary

def get_optimal_point(dictionary, basis):
    #---------idea------------#
    # -num of slack variables is number of ones in the basis
    # -we can count this and then if any ones occur in the basis before the index of the count
    # -they must be optimization variables and they are basic so they have a value
    vars = []
    slack_vars = 0
    for i in basis:
        if i == 1:
            slack_vars += 1
    opt_vars = len(basis) - slack_vars
    
    for i in range(1, opt_vars):
        if basis[i] == 1:
            for row in range(len(dictionary)):
                    if dictionary[row][i] == 1:
                        vars.append(dictionary[row][0])
        elif basis[i] == 0:
            vars.append(0)
        
    return vars

def solve_aux(auxillary, basis):
     #------solve auxillary problem loop until omega not in basis in degenerate case-----#
    method = "Largest_coeff"
    while basis[-1] == 1:                               #<- deal with case where omega in basis and degenerate pivot until optimal and its not
        auxillary, basis = solve(auxillary, basis, method)

        if basis[-1] == 1:                              #<- omega in basis and degenerate
            print("omega in basis\n")                 #<- IF OMEGA NOT DEGENERRATE MIGHT BE INFEASIBLE
            omega_row = None
            pivot_col = None
            method = "Blands"                           #<- to prevent cycling

                #---------find row omega is in to pivot out(pivot_row) if omega degenerate, if not degenerate -> infeasible---------#
            for row, eq  in enumerate(auxillary):      
                if eq[-1] == 1:                         #<- this row is omega row as al others have omega 0 since its basic
                    omega_row = row

            if omega_row == None:
                print("auxillary omega degenerate error")
                exit()

            if auxillary[omega_row][0] != 0:
                print('infeasible')
                exit()

            #--------find first available col to pivot in(pivot_col)--------#
            for col, val in enumerate(auxillary[omega_row]):                    #<-might not be degenerate could be infeasible
                if val != 0 and auxillary[0][col] != 0:
                    pivot_col = col
                    break

                
            if pivot_col == None:
                print("auxillary degenerate omega error") 
                exit()

            #-----do pivot-----------#
            auxillary, basis = do_pivot(auxillary, basis, pivot_col, omega_row)

    return(auxillary, basis)

def main():
    
    dictionary, basis = make_dictionary()

    #----------------------------
    #Check if initital dictionary feasible
    #solve aux problem if not 
    if not_feasible(dictionary):
        original_obj_function = copy.deepcopy(dictionary[0])
        auxillary, basis = create_aux_problem(dictionary, basis)

        print("auxillary")
        print(auxillary)
        print(basis)
        print()

        #------solve auxillary problem-----#
        auxillary, basis = solve_aux(auxillary, basis)

        print("auxillary solved")
        print(auxillary)
        print(basis)
        print()

        if get_obj_val(auxillary) != 0:
            print("infeasible")
            exit()

        #-------Construct feasible dictionary for original LP------#
        else:
            auxillary = np.delete(auxillary, -1, 1)         #<- delete omega col
            del basis[-1]                                   #<- delete omega col **can only do when were sure omega is not in basis

            dictionary = reintroduce(auxillary, basis, original_obj_function)
            dictionary, basis = solve(dictionary, basis, method = "Largest_coeff")
            

    else:
        dictionary, basis = solve(dictionary, basis, method = "Largest_coeff")
       

    #----------If were here dictionary is optimal----------#
    optimization_vars = get_optimal_point(dictionary, basis)     #<- will be a list
    print("optimal")
    print(float(get_obj_val(dictionary)))
    for val in optimization_vars:
        print(float(val), end = ' ')


    print('\nhi')


if __name__ == "__main__":
    main()
