memo = {}

def fast_pow(a, b, m):
    """Compute a^b mod m"""
    if (a, b, m) in memo:
        return memo[(a, b, m)]
    elif b == 1:
        memo[(a, b, m)] = a%m
        return memo[(a, b, m)]
    elif b%2:
        memo[(a, b, m)] = (a%m * fast_pow(a, b//2, m) * fast_pow(a, b//2, m))%m
        return memo[(a, b, m)]
    else:
        memo[(a, b, m)] = (fast_pow(a, b//2, m) * fast_pow(a, b//2, m))%m
        return memo[(a, b, m)]

print(fast_pow(20, 2001, 33))
print(pow(20, 2001, 33))