import sys
import copy
import numpy as np
from fractions import Fraction

def to_tableau(c, A, b):
    xb = [eq + [x] for eq, x in zip(A, b)]
    z = c + [0]
    arr = []
    #print (arr + [[]] + [[]])
    return xb + [z]


def main():
 
    c = [Fraction(1,5), Fraction(1,1), 0, 0, 0]
    A = [
        [-1, 1, 1, 0, 0],
        [ 1, 0, 0, 1, 0],
        [ 0, 1, 0, 0, 1]
    ]
    b = [2, 4, 4]
    
    tableau = to_tableau(c, A, b)
  
        
    auxillary = copy.deepcopy(tableau)           #<-----might be bad for performance
    for row in range(len(auxillary)):
        if row == 0:
            for entry in range(len(auxillary[row])):               #<--- zero out first row
                auxillary[row][entry] = 0
            auxillary[row] = auxillary[row] + [-1]                #<--- add negative omega col
        else:
            auxillary[row] = auxillary[row] + [-1]

    print(auxillary)

    l = [Fraction(1,5), Fraction(1,1), Fraction(3,4), Fraction(4,7)]
    l = np.array(l) / -1

    print(l)

if __name__ == "__main__":
    main()