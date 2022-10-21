# I pledge my honor that I have abided by the Stevens Honor System.

# Jason Qiu
# 2022-10-22


from random import randint
import json

def isPrime(n):
 
    # Corner cases
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5

    # All primes are 6n +/- 1, so start with i = 6(1) - 1 = 5, check n against i and i+2, then go to 6(2)-1 = 5+6
    while i * i <= n: # While i <= sqrt n
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i = i + 6
 
    return True

def gen_prime(n):
    p = randint(0, 1 << (n-1) - 1)
    try:
        while not (isPrime(p) and isPrime(2*p+1)):
            p = randint(0, 1 << (n-1) - 1)
        return p
    except IndexError: # If we generate a number too large, try again
        return gen_prime(n)

def find_generator(p, q):
    i = 2
    while i < p:
        if pow(i, q, p) == 1:
            return i
        i+=1


if __name__ == '__main__':
    # Generate p and q, write to file
    q = gen_prime(32)
    p = 2*q+1

    public_values = {"P":p, "Q": q, "g": 0}
    with open("public.json", "w") as f:
        json.dump(public_values, f)


    # Read from file, find g
    with open("public.json", "r") as f:
        public_values = json.load(f)

    g = find_generator(p, q)
    public_values["g"] = g
    with open("public.json", "w") as f:
        json.dump(public_values, f)

    # Diffie-Hellman Stuff
    for k, v in public_values.items():
        print(f"{k} = {v}")
    
    a = randint(0, q)
    b = randint(0, q)
    print(f"Alice's key a = {a}\nBob's key b = {b}")

    g_a = pow(g, a, p)
    g_b = pow(g, b, p)
    print(f"g^a = {g_a}\ng^b = {g_b}")

    k_a = pow(g_b, a, p)
    k_b = pow(g_a, b, p)
    assert k_a == k_b, "Keys for Alice and Bob do not match"
    print(f"key = {k_a}")