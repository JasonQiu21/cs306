# I pledge my honor that I have abided by the Stevens Honor System.

# Jason Qiu
# 2022-11-03

import hashlib
import sys
import random
from math import gcd
sys.setrecursionlimit(1000000)

def lcm(a, b):
    """lcm of a and b"""
    return a * b // gcd(a, b)

def totient(p, q):
    """Euler's totient for two primes p and q"""
    return (p-1) * (q-1)

# Adaptation from 
def egcd(a, b):
    """Implementation of gcd using Extended Euclidian Algorithm. 
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


# Adapted from lab7
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
    p = random.randrange(1 << (n-1), (1 << n) - 1)
    try:
        while not isPrime(p):
            p = random.randrange(1 << (n-1), (1 << n) - 1)
        return p
    except IndexError: # If we generate a number too large, try again
        return gen_prime(n)

# RSA
def gen_key():
    p = gen_prime(32)
    q = gen_prime(32)
    N = p*q
    _totient = totient(p, q)
    e = 65537
    d = modinv(e, _totient)
    return (e, N), (d, p, q)

if __name__ == '__main__':
    print("--------------------------------------------------RSA Keygen--------------------------------------------------")
    public, private = gen_key()
    print(f"Public key pair (e, N): {public}")
    print(f"Private key pair (d, p, q): {private}")

    # Signing
    print("--------------------------------------------------Message Signing--------------------------------------------------")
    message = "According to all known laws of aviation, there is no way a bee should be able to fly."

    digest_60 = bin(int(hashlib.sha256(message.encode('utf-8')).hexdigest(), 16))[:62] # :62 b/c of the characters '0b' at the prepended with bin

    print(f"Message: {message}")
    print(f"SHA256 digest (first 60 bits): {digest_60} = {hex(int(digest_60, 2))}") # 60 bits b/c small N (only 2^64)

    digest_60_signed = pow(int(digest_60, 2), private[0], public[1])
    print(f"digest signed: {hex(digest_60_signed)}")

    # Verifying
    print("--------------------------------------------------Valid Message and Signature Verification--------------------------------------------------")

    print(f"Received message: {message}")
    digest_60_receiever = bin(int(hashlib.sha256(message.encode('utf-8')).hexdigest(), 16))[:62] # :62 b/c of the characters '0b' at the prepended with bin
    print(f"SHA256 digest (first 60 bits): {digest_60_receiever} = {hex(int(digest_60_receiever, 2))}")

    print(f"Received signature {hex(digest_60_signed)}")
    digest_60_decrypted = pow(digest_60_signed, public[0], public[1])
    print(f"digest decrypted: {hex(digest_60_decrypted)}")
    assert bin(digest_60_decrypted) == digest_60_receiever, "Expected: valid signed message's decrypted signature matches digest of message. Received: Mismatch between signatures"
    print("Signature and hash of message match, message is verified.")

    print("--------------------------------------------------Altered Message Verification--------------------------------------------------")
    altered_message = "According to all known laws of aviation, bees should be able to fly."

    print(f"Received message: {altered_message}")
    digest_60_receiever = bin(int(hashlib.sha256(altered_message.encode('utf-8')).hexdigest(), 16))[:62] # :62 b/c of the characters '0b' at the prepended with bin
    print(f"SHA256 digest (first 60 bits): {digest_60_receiever} = {hex(int(digest_60_receiever, 2))}")

    print(f"Received signature {hex(digest_60_signed)}")
    digest_60_decrypted = pow(digest_60_signed, public[0], public[1])
    print(f"digest decrypted: {hex(digest_60_decrypted)}")
    assert bin(digest_60_decrypted) != digest_60_receiever, "Expected: invalid message's decrypted signature does not match digest of message. Received: Match between digests"
    print("Signature and hash of message are different, reject signature")

    print("--------------------------------------------------Altered Signature Verification--------------------------------------------------")
    altered_digest_60_signed = int(bin(digest_60_signed)[:-1] + ('1' if bin(digest_60_signed)[-1] == '0' else '0'), 2) # Flip last bit

    print(f"Received message: {message}")
    digest_60_receiever = bin(int(hashlib.sha256(message.encode('utf-8')).hexdigest(), 16))[:62] # :62 b/c of the characters '0b' at the prepended with bin
    print(f"SHA256 digest (first 60 bits): {digest_60_receiever} = {hex(int(digest_60_receiever, 2))}")

    print(f"Received signature {hex(altered_digest_60_signed)}")
    digest_60_decrypted = pow(altered_digest_60_signed, public[0], public[1])
    print(f"digest decrypted: {hex(digest_60_decrypted)}")
    assert bin(digest_60_decrypted) != digest_60_receiever, "Expected: invalid message's decrypted signature does not match digest of message. Received: Match between digests"
    print("Signature and hash of message are different, reject signature")


    


