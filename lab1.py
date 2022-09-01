# I pledge my honor that I have abided by the Stevens Honor System.

# Jason Qiu
# 2022-09-01

def extended_euclid_fronthalf(a, b):
    """Euclidian algorithm -- doesn't give coefficients, just first step"""
    if b%a:
        print(f"{b%a} =  {b} - {b//a}*{a}")
        extended_euclid_fronthalf(b%a, a)


def extended_euclid(a, b):
    """Implementation of gcd using Euler's Extended Algorithm. 
    Returns GCD g coefficients x and y of linear combination xa + yb"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_euclid(b % a, a)
        if y:
            print(f"{g} = {x - (b // a) * y}*{a} + {y}*{b}")
        return (g, x - (b // a) * y, y)

def gcd(a, b):
    g, x, y = extended_euclid(a, b)
    return g

extended_euclid_fronthalf(21, 30)
print("\n")
print(gcd(21, 30))