# I pledge my honor that I have abided by the Stevens Honor System.

# Jason Qiu
# 2022-09-21

from lab2 import no_memo_pow, fast_pow # Divide-and-conquer algorithm for modular exponentiation (implemented last week)
from random import randint
from time import time_ns

def faster_pow(a, b, m):
    """Compute a^b mod m"""
    result = 1
    prev = None
    x_i = a%m # x_0 = a%m
    for i in range(len(bin(b)) - 2): # Because bin returns string '0b{binary number}', we subtract the two characters from it
        if bool((b&(2**i))): # Get the ith bit from left
            result *= x_i
        prev = x_i
        x_i = (prev**2)%m # In general, x_i = x_{i-1}^2 (mod m)
    return result%m

if __name__ == '__main__':
    N = 100003
    # Generate two random ints such that 2^31 <= a,b < 2^32
    a = randint(2**31, 2**32-1)
    b = randint(2**31, 2**32-1)

    print(f"a = {a}\nb = {b}")

    for k, v in {'built-in':pow, 'precomputation': faster_pow, 'memoized divide-and-conque': fast_pow, 'divide-and-conquer': no_memo_pow}.items():
        print(f"Using {k} algorithm for modular exponentiation.", end="")
        try:
            start = time_ns()
            built_in = v(a, b, N)
            end = time_ns()
            print(f" Result: {built_in}. Time elapsed: {end-start} ns")
        except RecursionError:
            print(f" Result: recurtionError. Time elapsed: [N/A] ns")