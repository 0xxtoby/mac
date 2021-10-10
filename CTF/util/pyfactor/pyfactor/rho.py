from sympy import igcd as gcd

def pollard_rho(n, r=2, c=1, limit=10**6):
	i = 1
	x, y = r, (pow(r, 2, n)+c)%n
	g = gcd(y-x, n)
	while g == 1:
		if i >= limit:
			return n
		i += 1
		x = (pow(x, 2, n)+c) % n
		y = (pow(y, 2, n)+c) % n
		y = (pow(y, 2, n)+c) % n
		g = gcd(y-x, n)
	return g

def brent(n, r=2, c=1, limit=10**6):
	i = 1
	x = r
	y, k = r, 2
	while i < limit:
		i += 1
		x = (pow(x, 2, n) + c) % n
		g = gcd(x - y, n)
		if 1 < g < n:
			return g
		if i == k:
			y = x
			k *= 2
	return None

