import random
import time
import sympy
from math import log
from math import ceil
from sympy import igcd as gcd
from sympy import jacobi_symbol, isprime
from math import log
from random import randint


def v_lucas(P, r, n=1):
	bstr = bin(r).lstrip("0b")[1:]
	vkm1, vk = 2, P
	if r == 0:
		return vkm1
	if r == 1:
		return vk
	for b in bstr:
		if b == '0':
			vkm1 = (vk * vkm1 - P) % n
			vk = (vk * vk - 2) % n
		else:
			tmp = vkm1
			vkm1 = (vk * vk - 2) % n
			vk = (P*vk*vk - vk*tmp - P) % n 
	return vk


'''
	Williams p+1 
'''
def pp1(n, B=10**6, r=3, retries=1, verbose=False):
	while retries != 0:
		v = r
		for q in sympy.sieve.primerange(2, B):
			m = int(log(n, q))
			v = v_lucas(v, pow(q, m), n)
			g = gcd(v-2, n)
			if 1 < g < n:
				if not verbose:
					return g
				else:
					while g % 2 == 0:
						g //= 2
					return g, jacobi_symbol(r**2-4, g)
		r += random.randint(2, 5)
		retries -= 1
	if verbose:
		return None, None
	else:
		return None

