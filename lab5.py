# I pledge my honor that I have abided by the Stevens Honor System.

# Jason Qiu
# 2022-10-05
from math import ceil, sqrt

# From lab 1
def egcd(a, b):
    """Implementation of gcd using Euler's Extended Algorithm. 
    Returns GCD g coefficients x and y of linear combination xa + yb"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def bsgs(b, g, p):
    """
    Find discrete logarithm of b with base generator g and prime p
    If it doesn't exists (i.e. bad generator), return False
    """
    # What we're saying is g^x = b, and finding x = im+j
    m = ceil(sqrt(p))
    
    # Precompute g^j (mod P) for all 0 <= j < m
    g_to_j_power = []
    for j in range(m):
        if g_to_j_power: # if not empty, use previous element to more quickly compute power
            g_to_j_power.append((g_to_j_power[-1] * g)%p)
        else:
            g_to_j_power.append(pow(g, j, p))
    g_to_negm = (modinv(g, p))**m
    for i in range(m):
        if (b*g_to_negm**i)%p in g_to_j_power:
            # Return i*m + j
            return i*m + g_to_j_power.index((b*g_to_negm**i)%p)
    return False

if __name__ == '__main__':
    print(bsgs(14, 2, 19))
    print(bsgs(17, 2, 19))