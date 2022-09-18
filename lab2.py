# I pledge my honor that I have abided by the Stevens Honor System.

# Jason Qiu
# 2022-09-21

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

# Version with no memoization
def no_memo_pow(a, b, m):
    """Compute a^b mod m"""
    if b == 1:
        return a%m
    elif b%2:
        return (a%m * no_memo_pow(a, b//2, m) * no_memo_pow(a, b//2, m))%m
    else:
        return (no_memo_pow(a, b//2, m) * no_memo_pow(a, b//2, m))%m

if __name__ == '__main__':
    print(no_memo_pow(20, 2001, 33))
    print(fast_pow(20, 2001, 33))
    print(pow(20, 2001, 33))