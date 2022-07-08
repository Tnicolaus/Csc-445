import sys
import copy
from tkinter.ttk import Separator
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
  
    print(np.array(tableau[0]))
    for i, val in enumerate(np.array(tableau[0])):
        if i > 0 and val > 0:
            break
            #print("true")

    a = np.array([1,2,3,4,0], dtype=object)
    b = np.array(a)
    #print(b)
    a[0] = 2
    #print(a)
    a = np.delete(a, [-1])

    l = Fraction(1,1)
    l = l/2
    print(l)
    eq = np.array([
        [Fraction(1), Fraction(2)],
        [Fraction(3), Fraction(4)]
    ])

    obj_eq = np.array([[1,2,3,4],
                    [5,6,7,8],
                    [9,10,11,12]]
                    )
    print(eq[0][0])
    eq[0][0] = Fraction(0)
    print(eq)

    a = np.append(a,[1])
    #print(a)


if __name__ == "__main__":
    main()