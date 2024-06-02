import numpy as np

def linearSolve(A, b):

    A_inv = np.linalg.inv(A)  # A의 역행렬을 구함
    x = np.dot(A_inv, b) 
    return x

def main():

    A = np.array(np.random.randint(-10, 10, 9).reshape(3, 3))
    b = np.array(np.random.randint(-10, 10, 3).reshape(3, 1))
    print("A: ", A)
    print('b: ', b)
    
    x = linearSolve(A, b)
    print("x:", x)


if __name__ == "__main__":
    main()
