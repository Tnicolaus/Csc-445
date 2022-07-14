import sys
import copy
from tkinter.ttk import Separator
import numpy as np
from fractions import Fraction
from decimal import Decimal

def main():
 
    c = [Fraction(1,5), Fraction(1,1), 0, 0, 0]
    A = [
        [-1, 1, 1, 0, 0],
        [ 1, 0, 0, 1, 0],
        [ 0, 1, 0, 0, 1]
    ]
    b = [2, 4, 4]

    #print(b.extend([0,0,0]))
    line = '   \t     0.1    1.333  2     3.0\t4         5    \t \n'
    line = line.strip().split()

    for i in range(1, 4+1):
        print(i)
    #for char in line:
    #    if char == ' ' or char == '\t':

    #print(line)
  
    a = np.array([1,2,3,4,0], dtype=object)
    b = np.array(a)
    #print(b)
    a[0] = 2
    #print(a)
    a = np.delete(a, [-1])

    l = Fraction(1,1)
    l = l/2
    #print(l)
    eq = np.array([
        [Fraction(1), Fraction(2)],
        [Fraction(3), Fraction(4)]
    ])

    obj_eq = np.array([[1,2,3,4],
                    [5,6,7,8],
                    [9,10,11,12]]
                    )
    #print(Fraction(0) == 0)

    eq[0][0] = Fraction(0)
    #print(eq)

    a = np.append(a,[1])
    #print(a)

    m = 1.23495
    #m = round(m, 4)
    print('%.4f' % m)

if __name__ == "__main__":
    main()