import numpy as np

np.seterr(all='raise')


def model_function(t, A, K, C):
    return A * np.exp(K * t) + C

class InvalidDataVector(Exception):
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return "Dimension of x,y values must be larger than 1. %s" % self.msg


def _return_auxiliary_matrices_first_eq(x, y):
    A = [[0., 0.], [0., 0.]]
    B = [0., 0.]
    S = 0.
    for i in range(len(x)):
        A[0][0] += (x[i] - x[0]) ** 2
        A[0][1] += (x[i] - x[0]) * S
        A[1][0] += (x[i] - x[0]) * S
        A[1][1] += S ** 2
        B[0] += (y[i] - y[0]) * (x[i] - x[0])
        B[1] += (y[i] - y[0]) * S
        try:
            S += 0.5 * (y[i + 1] + y[i]) * (x[i + 1] - x[i])
        except IndexError:
            pass
    return A, B


def _return_auxiliary_matrices_second_eq(x, y, k):
    A = [[float(len(y)), 0.], [0., 0.]]
    B = [0., 0.]
    for i in range(len(y)):
        e = np.exp(k * x[i])
        A[0][1] += e
        A[1][0] += e
        A[1][1] += e ** 2
        B[0] += y[i]
        B[1] += y[i] * e
        return A, B


def _solve_first_equation(matrixA, matrixB):
    det = matrixA[0][0] * matrixA[1][1] - matrixA[0][1] * matrixA[1][0]
    A_inverse = [[matrixA[1][1] / det, -matrixA[0][1] / det], [-matrixA[1][0] / det, matrixA[0][0] / det]]
    k = A_inverse[1][0] * matrixB[0] + A_inverse[1][1] * matrixB[1]
    return k


def _solve_second_equation(matrixA, matrixB):
    det = matrixA[0][0] * matrixA[1][1] - matrixA[0][1] * matrixA[1][0]
    A_inverse = [[matrixA[1][1] / det, -matrixA[0][1] / det], [-matrixA[1][0] / det, matrixA[0][0] / det]]

    c = A_inverse[0][0] * matrixB[0] + A_inverse[0][1] * matrixB[1]
    a = A_inverse[1][0] * matrixB[0] + A_inverse[1][1] * matrixB[1]
    return a, c

"""
def exp_fit(x, y):
    # 1. equation
    if len(x)<=2:
        raise InvalidDataVector("Current data vector length is: %s" % len(x))
    A, B = _return_auxiliary_matrices_first_eq(x, y)
    k = _solve_first_equation(A, B)

    # 2. equation
    A, B = _return_auxiliary_matrices_second_eq(x, y, k)
    a, c = _solve_second_equation(A, B)
    return a, k, c
"""

def exp_fit(x, y):
    # 1. equation
    A = [[0., 0.], [0., 0.]]
    B = [0., 0.]
    S = 0.
    for i in range(len(x)):
        A[0][0] += (x[i] - x[0]) ** 2
        A[0][1] += (x[i] - x[0]) * S
        A[1][0] += (x[i] - x[0]) * S
        A[1][1] += S ** 2
        B[0] += (y[i] - y[0]) * (x[i] - x[0])
        B[1] += (y[i] - y[0]) * S
        try:
            S += 0.5 * (y[i + 1] + y[i]) * (x[i + 1] - x[i])
        except IndexError:
            pass
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    A_inverse = [[A[1][1] / det, -A[0][1] / det], [-A[1][0] / det, A[0][0] / det]]
    k = A_inverse[1][0] * B[0] + A_inverse[1][1] * B[1]


    # 2. equation
    A = [[float(len(y)), 0.], [0., 0.]]
    B = [0., 0.]
    for i in range(len(y)):
        e = np.exp(k * x[i])
        A[0][1] += e
        A[1][0] += e
        A[1][1] += e ** 2
        B[0] += y[i]
        B[1] += y[i] * e

    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    A_inverse = [[A[1][1] / det, -A[0][1] / det], [-A[1][0] / det, A[0][0] / det]]

    c = A_inverse[0][0] * B[0] + A_inverse[0][1] * B[1]
    a = A_inverse[1][0] * B[0] + A_inverse[1][1] * B[1]
    return a, k, c
