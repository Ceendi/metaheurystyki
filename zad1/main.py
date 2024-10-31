import math
import random


# T = 500
# a(T) = 0.999 * T
# k = 0.1
# M = 3000
def first_function(x):
    if -105 < x < -95:
        return -2 * math.fabs(x + 100) + 10
    elif 95 < x < 105:
        return -2.2 * math.fabs(x - 100) + 11
    else:
        return 0


# T = 5
# a(T) = 0.997 * T
# k = 0.1
# M = 1200
def second_function(x):
    return x * math.sin(10 * math.pi * x) + 1


def randomize(a, b):
    return random.uniform(a, b)


def annealing(T, a, M, k, r1, r2, fun):
    x = randomize(r1, r2)
    f = fun(x)
    for i in range(M):
        x_new = randomize(x - 2 * T, x + 2 * T)
        while x_new > r2 or x_new < r1:
            x_new = randomize(x - 2 * T, x + 2 * T)
        print(T)
        f_new = fun(x_new)
        if f_new > f:
            f = f_new
            x = x_new
        elif math.exp(-(f - f_new) / (k * T)) > randomize(0, 1):
            f = f_new
            x = x_new
        T *= a

    return x, f


#print(annealing(500, 0.999, 3000, 0.1, -150, 150, first_function))
print(annealing(5, 0.997, 1200, 0.1, -1, 2, second_function))
