import math
from random import randint

try:
	import sympy
	from sympy import nextprime
	from sympy import sieve
	from sympy import mod_inverse
	from sympy import igcd as gcd
except ImportError:
	print("Please install SymPy Library")
	exit(1)

#==================================
#	Parallel Inverse Modulo N
#==================================
def parallel_invert(a_list, n):
	'''
	b[] 是 a[] 的模n的逆元，否则给出n的非平凡因子
	参考：Henri Cohen. A Course in Computational Algebratic Number Theory(Page 489)'''

	k = len(a_list)
	b_list = a_list[:]
	for i in range(k-1):
		b_list[i+1] = (b_list[i] * b_list[i+1]) % n

	try:
		inv = mod_inverse(b_list[-1], n)
	except:
		g = gcd(b_list[-1], n)
		if 1 < g < n:
			return g, True
		else:
			for item in a_list:
				g = gcd(item, n)
				if 1 < g < n:
					return g, True
			# 希望不要出现这个状况
			return None, True

	for i in range(k - 1, 0, -1):
		b_list[i] = (inv * b_list[i - 1]) % n
		inv = (inv * a_list[i]) % n
	b_list[0] = inv

	return b_list, False



#==================================
#	Parallel Add Modulo N
#==================================
def parallel_add(p1_list, p2_list, a_list, n):
	'''
	p1_list, p2_list 为多个椭圆曲线上的点的列表
	a_list 是多个椭圆曲线的参数
	n 为待分解的合数'''
	k = len(p1_list)
	m1_list = []
	m2_list = []
	res = []
	
	for i in range(k):
		x1, y1 = p1_list[i]
		x2, y2 = p2_list[i]
		a = a_list[i]
		if p1_list[i] == p2_list[i]:
			m1_list.append((3 * x1 * x1 + a) % n)
			m2_list.append(2 * y1 % n)
		else:
			m1_list.append((y2 - y1) % n)
			m2_list.append((x2 - x1) % n)
			
	inv_list, flag = parallel_invert(m2_list, n)
	if flag:
		return inv_list, True
	
	for i in range(k):
		x1, y1 = p1_list[i]
		x2, y2 = p2_list[i]
		m = m1_list[i] * inv_list[i] % n
		x3 = (m * m - x1 - x2) % n
		y3 = (m*(x1 - x3) - y1) % n
		res.append((x3, y3))
	return res, False


#==================================
#	Parallel Add Modulo N
#==================================
def parallel_mul(k, p_list, a_list, n):
	'''
	多条椭圆曲线并行数乘'''
	if k == 1:
		return p_list, False
	
	k -= 1
	length = len(p_list)
	res_list = p_list[:]
	while k > 0:
		if (k&1):
			res_list, flag = parallel_add(res_list, p_list, a_list, n)
			if flag:
				return res_list, True
		k >>= 1
		p_list, flag = parallel_add(p_list, p_list, a_list, n)
		if flag:
			return p_list, True
	return res_list, False


#===================================
#	Generate Elliptic-Curve
#===================================
def parallel_generate_elliptic_curve(n, k):
	'''
	一次生成k条形如 y^2 = x^3 + a*x + 1 曲线
	初始点P = (0, 1)'''
	sigma = randint(6, int(math.log(n))**2)
	a_list = list(range(sigma, sigma+k, 1))
	return a_list
#=========================================
#	Main Algorithm
#=========================================			
def parallel_ecm(n, verbose=False, digits=20, limits=None):
	'''
	并行ECM
	素因子规模(log10) 光滑界B		曲线数C
			12			125			50
			13			250			53
			14			500			57	
			15			830			62
			16			1500		68
			17			2500		75
			18			4200		85
			19			6500		100
			20			10000		120
			21			15000		145
			22			22000		175
			23			32000		210
			24			45000		250	
			25			65000		300
			26			85000		400
			27			115000		500
			28			155000		650
			29			205000		750
			30			275000		950
	'''
	B = [125, 250, 500, 830, 1500, 2500, 4200, 6500, 10000, \
		 15000, 22000, 32000, 45000, 65000, 85000, 115000, \
		 155000, 205000, 275000]
	C = [50, 53, 57, 62, 68, 75, 85, 100, 120, 145, 175, 210, \
		 250, 300, 400, 500, 650, 750, 950]
	
	index = max(digits, 13)-13
	if limits != None:
		limits = min(limits, len(B)+1)
	failed = False
	while True:
		# 
		for bound, k in zip(B[index:limits], C[index:limits]):
			if verbose:
				print("B =", bound, "C =", k)

			# 生成椭圆曲线参数 
			p_list = [(0,1) for _ in range(k)]
			a_list = parallel_generate_elliptic_curve(n, k)

			# 椭圆曲线的点的数乘 (p1^a1 p2^a2 ... pk^ak) * P 
			for p in sieve.primerange(2, bound):
				e = int(math.log(bound, p))
				p_list, founded = parallel_mul(pow(p, e), p_list, a_list, n)
				if founded and p_list != None:
					if verbose:
						print(a_list)
					return p_list
				elif p_list == None:
					# 椭圆曲线上的点P, 存在k 使得kP = (0, 0)
					# 算法失败 设置failed = True
					failed = True
					break

			# 算法失败，需要跳出循环, 重新选择椭圆曲线参数
			if failed:
				failed = False
				break
			index += 1
		if index >= limits:
			break
	return None

