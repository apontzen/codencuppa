"""sieve.py

Author: Andrew Pontzen
Date: 3 December 2024

"""

def Sieve(X):
    """Implements the sieve"""

    a = [1] * (X + 1) # initialize list
    a[0] = a[1] = 0 # update initialization of 0 and 1 element
    for i in range(2, int(X ** 0.5) + 1): # loop over i
        if a[i]:
            for j in range(i * i, X + 1, i):
                # set all these elements to 0
                a[j] = 0

    # use a list comprehension to get the results
    results = [n for n, v in enumerate(a) if v]

    # print results
    print(results)

Sieve(100)
