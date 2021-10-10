import sympy
from sympy import nextprime
from sympy import igcd as gcd
from math import log
from datetime import datetime
from random import randint
import time

def pm1(n, B=10**6, r=2):
    b = r
    for q in sympy.sieve.primerange(2, B):
        m = int(log(n, q))
        b = pow(b, pow(q, m), n)
        g = gcd(b-1, n)
        if 1 < g < n:
            return g
    return None


