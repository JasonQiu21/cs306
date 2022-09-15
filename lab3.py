from lab2 import no_memo_pow

def faster_pow(a, b, m):
    """Compute a^b mod m"""
    result = 1
    prev = None
    for i in range(m):
        if i == 0:
            x_i = a%m
        else:
            x_i = (prev**2)%m
        if bool((b&(2**i))): # Get the ith bit
            result *= x_i
        prev = x_i
    return result%m

