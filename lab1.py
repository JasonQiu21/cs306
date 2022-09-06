# I pledge my honor that I have abided by the Stevens Honor System.

# Jason Qiu
# 2022-09-01

def extended_euclid_fronthalf(a, b):
    """Euclidian algorithm -- doesn't give coefficients, just first step"""
    if b%a:
        print(f"{b%a} =  {b} - {b//a}*{a}")
        extended_euclid_fronthalf(b%a, a)


def extended_euclid(a, b, print_steps=True):
    """Implementation of gcd using Euler's Extended Algorithm. 
    Returns GCD g coefficients x and y of linear combination xa + yb"""
    if a == 0:
        # Base case: gcd(0, b) = b = n*0 + 1*b for all n
        return (b, 0, 1)
    else:
        # Recursive case: gcd(a,b) = gcd(b%a, a) (remember, b = b%a + n*a for some n = b//a (// is integer divide)
        # then,
        # gcd(a,b) = gcd(b%a, a) = y*b%a + x*b 
        # = y*(b-(b//a)*a) + x*b = y*b-y*(b//a)*a + x*a = y*b + (x-(b//a)*y)*a
        g, y, x = extended_euclid(b % a, a, print_steps)
        if y and print_steps:
            print(f"{g} = {x - (b // a) * y}*{a} + {y}*{b}")
        return (g, x - (b // a) * y, y)

def gcd(a, b):
    extended_euclid_fronthalf(a, b)
    print("\n")
    g, x, y = extended_euclid(a, b)
    return g

def mod_inv(a, b):
    """Modular inverse of a mod b"""
    g, x, y = extended_euclid(a, b, print_steps=False)
    # gcd(a, b) = x*a + y*b = 1 ==> x*a = 1 (mod b) ==> a^-1 = x (mod b)
    if g != 1:
        raise Exception("Modular inverse does not exist")
    else:
        return x%b

print(gcd(23, 30))
print(f"mod inv: {mod_inv(23, 30)}")
print("\n")
print(gcd(1237, 56789))
print(f"mod inv: {mod_inv(1237, 56789)}")