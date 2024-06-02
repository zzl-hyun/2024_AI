import numpy as np

def leastsSquareSolve(A, b):

    pseudoInv = np.linalg.pinv(A)
    x = np.dot(pseudoInv, b) 
    return x

def main():

    A = np.array(np.random.randint(-10, 10, 6).reshape(3, 2))
    b = np.array(np.random.randint(-10, 10, 3).reshape(3, 1))
    print("A: ", A)
    print('b: ', b)
    
    x = leastsSquareSolve(A, b)
    print("x:", x)


if __name__ == "__main__":
    main()
