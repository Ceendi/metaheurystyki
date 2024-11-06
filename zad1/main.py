import math
import random
import matplotlib.pyplot as plt
import numpy as np


def first_function(x):
    if -105 < x < -95:
        return -2 * math.fabs(x + 100) + 10
    elif 95 < x < 105:
        return -2.2 * math.fabs(x - 100) + 11
    else:
        return 0


def second_function(x):
    return x * np.sin(10 * math.pi * x) + 1


def randomize(a, b):
    return random.uniform(a, b)


def annealing(T, a, M, p, k, r1, r2, function):
    x = randomize(r1, r2)
    f = function(x)

    for i in range(M):
        for j in range(p):
            x_new = randomize(x - 2 * T, x + 2 * T)
            while x_new > r2 or x_new < r1:
                x_new = randomize(x - 2 * T, x + 2 * T)

            f_new = function(x_new)
            if f_new > f:
                f = f_new
                x = x_new
            elif math.exp(-(f - f_new) / (k * T)) > randomize(0, 1):
                f = f_new
                x = x_new
        T *= a

    return x, f


# perfect dla x=100 y=11
param_1 = {
    "T": 500,
    "a": 0.999,
    "M": 3000,
    "p": 5,
    "k": 0.1,
    "r1": -150,
    "r2": 150,
    "function": first_function
}


# perfect dla x=1.850547 y=2.85027376656965
param_2 = {
    "T": 5,
    "a": 0.997,
    "M": 1200,
    "p": 5,
    "k": 0.1,
    "r1": -1,
    "r2": 2,
    "function": second_function
}


def start(params, attempts=10):
    results = []
    for i in range(attempts):
        x, f = annealing(**params)
        results.append((x, f))
        print(f"Iteration {i}: x={x}, y={f}")
    return results


print("Pierwsza funkcja: ")
start(param_1)

print("Druga funkcja:")
start(param_2)
