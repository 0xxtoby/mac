import math
from math import sqrt, log2, ceil, floor

import random
from random import randint

import sys
import time

from datetime import datetime

import pickle
import os
import hashlib

try:
	import sympy
	from sympy import igcd as gcd
	from sympy import nextprime, isprime, jacobi_symbol
	from sympy import mod_inverse, sqrt_mod, integer_nthroot
except ImportError:
	print("请安装SymPy库!!")
	sys.exit(1)



############################################################################
#
#			常数、结构定义
#
############################################################################

SIQS_TRIAL_DIVISION_EPS = 25		#
SIQS_IGNORE_PRIME_BOUND = 20		#
SIQS_MIN_PRIME_POLYNOMIAL = 400		#
SIQS_MAX_PRIME_POLYNOMIAL = 4000	#

#========================================================
#	多项式
#========================================================
class Polynomial:
	"""
	a, b: (a*x + b)^2
	
	coeff:  ----k
			\
			 \	  coeff[i] * x^i
			 /
		    ----i = 0
	"""
	def __init__(self, coeff=[], a=None, b=None):
		self.coeff = coeff
		self.a = a
		self.b = b

	def eval(self, x):
		res = 0
		for a in self.coeff[::-1]:
			res *= x
			res += a
		return res
#==========================================================
# SIQS 因子基
#==========================================================
class Factor_Base_Prime:
	"""
	因子基:
		p: jacobi_symbol(n / p) = 1的素数
		lp: log2(p)
		tmem:  t^2 = n (mod p)的解
		soln1, soln2: (a*x+b)^2 = n (mod p)的解
		a_inv: a_inv * a = 1(mod p)"""

	def __init__(self, p, tmem, lp):
		self.p = p
		self.soln1 = None
		self.soln2 = None
		self.tmem = tmem
		self.lp = lp
		self.ainv = None

############################################################################
#
#	    	工具函数
#
############################################################################
def lowest_set_bit(a):
	'''
	二进制数 a>0 从最低位开始 '0' 的个数
	例: a = 0x101101100 -> 2
		a = 0x111100110 -> 1
		a = 0x000000001 -> 0'''
	b = (a & -a)
	low_bit = -1
	while (b):
		b >>= 1
		low_bit += 1
	return low_bit
	

def is_quadratic_residue(a, p):
	"""
	如果 a 是 p 的二次剩余，返回True, 否则返回false"""
	if p == 2:
		return True
	return jacobi_symbol(a, p) == 1
	
def int_sqrt(n):
	'''
	sqrt(n)取整'''
	s, _ = integer_nthroot(n, 2)
	return s
	
def tdiv(num, factor_base):
	'''
	使用因子基中的 factor_base 除 num
		num = (-1)^e[-1] * p[0]^e[0] * ... * p[k]^e[k] 
	返回:
		divisors_idx数组 
			divisors_idx[k] = (i, exp) 
			i 	表示因子基 factor_base 的索引，i=-1对应的数是-1
			exp 表示 num分解式中 素数factor_base[i].p的个数的奇偶性，
			    偶数为0，奇数为1
	'''
	if num < 0:
		divisors_idx = [(-1, 1)]
	else:
		divisors_idx = [(-1, 0)]
	for i, fb in enumerate(factor_base):
		if num % fb.p == 0:
			# exp 统计 num 的素因子分解中 fb.p 的个数的奇偶性
			exp = 0
			while num % fb.p == 0:
				num //= fb.p
				exp ^= 1
			divisors_idx.append((i, exp))
		if num == 1:
			return divisors_idx
	return None

##############################################################################
#
#			GF(2) 上的 齐次线性方程组、矩阵 求解
#
##############################################################################

#=====================================================
#	构建矩阵
#=====================================================
def siqs_build_matrix(factor_base, smooth_relations):
	'''
		构建矩阵:
		行数 = 因子基的大小+1，列数 = 光滑数的数量
		 v1 v2 v3     vi
		+-			   -+
	-1	| 1 0  1 ...  1 |
	p1	| 1	1  0 ...  0	|	
		|		 ...	|
	pi	| 0 1  0 ...  0 |
		+-			   -+

		在python中使用一维列表“转置”存储该矩阵:
		
		[ 0x11...0, 
		  0x01...0, 
		  0x10...0,
		  ..., 
		  0x10...0]
		
		返回：
			矩阵matrix，行数row_size， 列数col_size
			(row_size > col_size)
	'''
	col_size = len(factor_base)+1
	mat = []
	for v in smooth_relations:
		mi = [0 for _ in range(col_size)]
		for j, exp in v[2]:
			mi[j] = exp
		mat.append(mi)
		
	row_size = len(mat)
	cols_binary = ["" for _ in range(col_size)]
	for mi in mat:
		for j, mij in enumerate(mi):
			cols_binary[j] += "1" if mij else "0"
	matrix=[int(cols_bin[::-1], 2) for cols_bin in cols_binary]
	
	return matrix, row_size, col_size
	
#=================================================
#	求解 齐次线性方程组
#=================================================
def siqs_solve_matrix(matrix, row, col):
	
	row_marked = [False for _ in range(row)]
	pivots = [-1 for _ in range(col)]
	for j in range(col):
		i = lowest_set_bit(matrix[j]) if matrix[j] != 0 else -1
		if i >= 0:
			pivots[j] = i
			row_marked[i] = True
			for k in range(col):
				if k != j and (matrix[k] >> i) & 1:
					matrix[k] ^= matrix[j]

	perf_squares = []
	for i in range(row):
		if not row_marked[i]:
			perfect_sq_indices = [i]
			for j in range(col):
				if (matrix[j] >> i) & 1:  
					perfect_sq_indices.append(pivots[j])
			perf_squares.append(perfect_sq_indices)
	return perf_squares

#=====================================================
#	找出非平凡因子
#=====================================================
def siqs_find_factors(n, perfect_squares, smooth_relations):

	for square_indices in perfect_squares:
		left = 1
		right = 1
		for i in square_indices:
			left *= smooth_relations[i][0]
			right *= smooth_relations[i][1]
		right = int_sqrt(right)
		assert (left**2) % n == (right**2) % n
		g = gcd(left - right, n)
		if 1 < g < n:
			return g, n//g
	return None, None

###############################################################################
#
#							SIQS 初始化
#
###############################################################################

#=================================================
#	初始化 因子基大小、筛区间
#=================================================
def siqs_init(n):
	'''
	输入：
		n: 奇合数
	输出:
		factor_base: 因子基
		M: 筛区间[-M, M]
	'''
	
	d = len(str(n))
		
	
	if d <= 52:
		M = 10**5
	elif d <= 88:
		M = 10**5 * 3
	else:
		M = 10**5 * 9
	
	if d <= 34:
		base_size = 200
	elif d <= 36:
		base_size =  300
	elif d <= 38:
		base_size =  400
	elif d <= 40:
		base_size =  500
	elif d <= 42:
		base_size =  600
	elif d <= 44:
		base_size =  700
	elif d <= 48:
		base_size =  1000
	elif d <= 52:
		base_size =  1200
	elif d <= 56:
		base_size =  2000
	elif d <= 60:
		base_size =  4000
	elif d <= 66:
		base_size =  6000
	elif d <= 74:
		base_size =  10000
	elif d <= 80:
		base_size =  30000
	elif d <= 88:
		base_size =  50000
	elif d <= 94:
		base_size =  60000
	else:
		base_size =  100000
	
	factor_base = []
	for p in sympy.sieve.primerange(2, 10**6):
		if is_quadratic_residue(n, p):
			t = sqrt_mod(n, p)
			lp = round(log2(p))
			factor_base.append(Factor_Base_Prime(p, t, lp))
			if len(factor_base) >= base_size:
				break
	return factor_base, M


################################################################################
#
#							SIQS 多项式生成
#
###############################################################################

#================================================
#	生成第一个多项式
#================================================
def siqs_generate_poly(n, M, factor_base):
	'''
	描述: 生成多项式 
		  g(a, b, x) = (ax+b)^2 - next
	   和 h(a, b, x) = ax + b'''
	   
	# a = p[min_index] ... p[max_index] 之间的若干个随机素数乘积
	# p[min_index] >= SIQS_MIN_PRIME_POLYNOMIAL
	# p[max_index] >  SIQS_MAX_PRIME_POLYNOMIAL
	# max_index - min_index >= 20
	min_index = None
	max_index = None
	for index, fb in enumerate(factor_base):
		if min_index is None and fb.p >= SIQS_MIN_PRIME_POLYNOMIAL:
			min_index = index
		if max_index is None and fb.p > SIQS_MAX_PRIME_POLYNOMIAL:
			max_index = index - 1
			break
	
	# 如果因子基太小, max_index = 因子基长度
	# 				  min_index = min(5, min_index)
	if max_index is None:
		max_index = len(factor_base) - 1
	if min_index is None:
		min_index = 5
	elif max_index - min_index < 20:
		min_index = min(min_index, 5)
	
	# a 约等于 sqrt(2*n) / M
	target = int_sqrt(2 * n) // M
	target1 = target // int_sqrt((factor_base[min_index].p + 
								  factor_base[max_index].p))
	# a = q[1...s]的乘积
	best_plist, best_a, best_ratio = None, None, None
	for _ in range(30): 
		a = 1
		index_plist = []

		while a < target1:
			i = 0
			while i == 0 or i in index_plist:
				i = random.randint(min_index, max_index)
			a *= factor_base[i].p
			index_plist.append(i)

		ratio = a / target
		
		if best_ratio is None \
			or (0.9 <= ratio < best_ratio) \
			or (best_ratio < 0.9 and ratio > best_ratio):
			best_plist = index_plist
			best_a = a
			best_ratio = ratio
	a = best_a
	index_plist = best_plist
	s = len(index_plist)
	
	#计算 B[0...s-1]
	#	B[l]^2 = n (mod q[l]) 且 B[l] = 0 (mod q[j]), j != l
	B = []
	for l in range(s):
		fb_l = factor_base[index_plist[l]]
		ql = fb_l.p
		gamma = (fb_l.tmem * mod_inverse(a // ql, ql)) % ql
		if 2*gamma > ql:
			gamma = ql - gamma
		B.append(a // ql * gamma)
	
	b = sum(B) % a
	origin_b = b
	if (2 * b > a):
		b = a - b
	# 多项式 g = (ax+b) - n = a^2x + 2abx + b^2 - n
	# 多项式 h = ax+b
	g = Polynomial([b * b - n, 2 * a * b, a * a], a, origin_b)
	h = Polynomial([b, a])
	for fb in factor_base:
		if a % fb.p != 0:
			fb.ainv = mod_inverse(a, fb.p)
			fb.soln1 = (fb.ainv * (fb.tmem - b)) % fb.p
			fb.soln2 = (fb.ainv * (-fb.tmem - b)) % fb.p

	return g, h, B


#================================================
#	生成剩下的多项式
#================================================
def siqs_next_poly(n, factor_base, i, g, B):
	'''
	描述:
		g, i 表示第i个多项式 g
		该函数生成第i+1个多项式, 1 <= i <= 2^(s-1)-1'''
	v = lowest_set_bit(i) + 1
	z = -1 if ceil(i / (2 ** v)) % 2 == 1 else 1
	b = (g.b + 2 * z * B[v - 1]) % g.a
	a = g.a
	origin_b = b
	if (2 * b > a):
		b = a - b

	g = Polynomial([b * b - n, 2 * a * b, a * a], a, origin_b)
	h = Polynomial([b, a])
	for fb in factor_base:
		if a % fb.p != 0:
			fb.soln1 = (fb.ainv * (fb.tmem - b)) % fb.p
			fb.soln2 = (fb.ainv * (-fb.tmem - b)) % fb.p

	return g, h
######################################################################
#
#						SIQS 筛选与试除
#	
######################################################################

#=======================================================
#	SIQS 区间[-M, M]筛选
#=======================================================
def siqs_sieve(factor_base, M):
	'''
	在区间[-M, M]标记光滑数
	用 sieve_array[i+M] 表示 i
	sieve_array[0]   -> -M
	sieve_array[1]   -> -M+1
	...
	sieve_array[M] 	 -> 0
	sieve_array[M+1] -> 1'''
	sieve_array = [0 for _ in range(2*M+1)]
	for fb in factor_base:
		if fb.soln1 != None:
			p = fb.p
			# 为了加快速度，允许一定的误差
			# 设置SIQS_IGNORE_PRIME_BOUND的下界
			# 大于下界的素数才在数组sieve_array上做标记
			if p > SIQS_IGNORE_PRIME_BOUND:
				# 筛 (ax+b)^2 - n mod p 的第一个解
				start = fb.soln1 - ((M + fb.soln1) // p) * p
				lp = fb.lp
				for i in range(start + M, 2 * M + 1, p):
					sieve_array[i] += lp
					
				# 筛 (ax+b)^2 - n mod p 的第二个解
				start = fb.soln2 - ((M + fb.soln2) // p) * p
				lp = fb.lp
				for i in range(start + M, 2 * M + 1, p):
					sieve_array[i] += lp
	return sieve_array

#=======================================================
#	SIQS 区间[-M, M]试除
#=======================================================
def siqs_trial_division(n, sieve_array, factor_base, smooth_relations, 
						g, h, M, required):
	'''
	描述：根据sieve_array数组，使用试除法找光滑数
	输入:
		n: 奇合数
		sieve_array: 标记的筛区间数组
		factor_base: 分解基
		smooth_relations: 光滑关系数组
		g: 多项式 (ax+b)^2 - n
		h: 多项式 ax+b
		M: 表示筛区间[-M, M]
		required: 目标需要的光滑数
	输出:
		True: len(smooth_relations) >= required
		False: len(smooth_relations) < required
	备注:
		smooth_relations[i] 存储一个三元组(多项式 h的值, 多项式 g的值, 数组 divisors_idx)
		数组 divisors_idx 的含义与 工具函数tdiv 中的相同
	'''
	sqrt_n = int_sqrt(n)
	# 为了加快速度，允许一定的误差
	# sum(log2(p), 2<= 素数p < 20) < 24
	# 因此设置误差 SIQS_TRIAL_DIVISION_EPS = 25
	# 然后再进行试除
	limit = int(log2(M * sqrt_n)) - SIQS_TRIAL_DIVISION_EPS
	for (i, sa) in enumerate(sieve_array):
		if sa >= limit:
			# 数组sieve_array[0...2*M+1] 对于 区间[-M, M]
			# 因此sieve_array的下标 i 表示 数 x = i - M
			x = i - M
			g_value = g.eval(x)

			# 试除法判断是否光滑
			# 如果不是光滑数，返回None
			divisors_idx = tdiv(g_value, factor_base)
			
			#将光滑关系存入数组smooth_relations
			if divisors_idx is not None:
				smooth_relations.append((h.eval(x), g_value, divisors_idx))
				if (len(smooth_relations) >= required):
					return True
	return False


####################################################################
#
#				SIQS 主程序
#
#####################################################################

#=======================================
#	SIQS 算法实现
#=======================================
def siqs_factor(n, past_relations=[], gui_prog=None):
	'''
	SIQS 算法实现
	输入:
		n: 待分解的合数
		past_relations: 已经搜集到的光滑数
	输出:
		factor1, factor2: n的两个非平凡因子
	备注:
		past_relations[i] 存储的三元组与siqs_trial_division函数中的smooth_relations相同
		数组 divisors_idx 的含义与 工具函数tdiv 中的相同
	'''
	factor_base, M = siqs_init(n)
	required = len(factor_base) + 10
	smooth_relations = past_relations
	cnt = 0 # 存储光滑数的数量
	i = 0   # 多项式的索引序号
	
	while True:
		# 算法第一阶段：搜集光滑数
		# required 为目标搜集光滑数数量
		target = required - len(smooth_relations)
			
		if target > 0:
			finish = False
		else:
			finish = True
		
		if gui_prog is not None:
			gui_prog["maximum"] = required
			gui_prog["value"] = len(smooth_relations)
		
		print("******************************************")
		print("    Step 1: Finding smooth relations")
		print("******************************************")
		while not finish:
			# i = 0 生成第一个多项式
			if i == 0:
				g, h, B = siqs_generate_poly(n, M, factor_base)
			# 1 <= i <= 2**s - 1 生成下一个多项式
			else:
				g, h = siqs_next_poly(n, factor_base, i, g, B)
			i += 1
			# i >= 2**s 计数器i归零，准备生成新的多项式
			if i >= 2**(len(B) - 1):
				i = 0
			
			# 寻找光滑数
			# 1. 区间[-M, M]上标记 筛法数组sieve_array
			sieve_array = siqs_sieve(factor_base, M)
			
			# 2. 试除阶段
			finish = siqs_trial_division(
				n, sieve_array, factor_base, smooth_relations,
				g, h, M, required)

			if (len(smooth_relations) >= required or
				i % 8 == 0 and len(smooth_relations) > cnt):
				print("%d/%d progress." %
					  (len(smooth_relations), required))
				cnt = len(smooth_relations)
				if gui_prog is not None:
					gui_prog['value'] = cnt
		
		# 算法第二阶段
		# 求解GF(2)上的齐次线性方程组
		# 找到 x^2 = y^2 (mod n) 
		print("******************************************")
		print("    Step 2: Solving GF(2) Matrix")
		print("******************************************")		
		matrix, row, col = siqs_build_matrix(factor_base, smooth_relations)
		perfect_squares = siqs_solve_matrix(matrix, row, col)
		factor1, factor2 = siqs_find_factors(n, perfect_squares, smooth_relations)
		
		if factor1 != None:
			#print("Factors founded: ", factor1, "("+ str(len(str(factor1)))+"digits)")
			#print("Factors founded: ", factor2, "("+ str(len(str(factor2)))+"digits)")
			return factor1, factor2
		else:
			required += 5
			if gui_prog is not None:
				gui_prog["maximum"] = required

#========================================================
#	SIQS 调用主程序
#========================================================
def siqs_main(n, store=True, gui_prog=None):
	'''
	描述：
		该程序支持:
			*中断当前运算过程*
			*恢复上次分解的过程*
		用户可以在程序运行过程中，随时Ctrl-C中断，
	下次分解同一个合数时，该函数先从临时文件中读取
	上次分解过程	存储在硬盘中的光滑数关系，然后
	再继续进行二次筛法。
	
	store：如果为True，则分解结束，不删除临时文件
	'''
	
	# 寻找并读取临时存储文件
	if not os.path.exists("tmp"):
		os.mkdir("tmp")
	
	n_tag = hashlib.sha1(str(n).encode('utf-8')).hexdigest()
	past_relations = []
	tmpfile_path = "./tmp/"+n_tag
	tmpfile_exist = False
	
	if os.path.exists(tmpfile_path):
		tmpfile_exist = True
		tmp_file = open(tmpfile_path, "rb")
		past_relations = pickle.load(tmp_file)
		tmp_file.close()
	
	
	try:
		factor1, factor2 = siqs_factor(n, past_relations, gui_prog)
		# 删除临时文件
		if tmpfile_exist and not store:
			os.remove(tmpfile_path)
		# store为True, 保存临时文件
		elif store:
			tmp_file = open(tmpfile_path, "wb")
			pickle.dump(past_relations, tmp_file)
			tmp_file.close()
			
		return factor1, factor2
	except (KeyboardInterrupt, Exception):
		# 创建临时文件
		tmp_file = open(tmpfile_path, "wb")
		pickle.dump(past_relations, tmp_file)
		tmp_file.close()
		raise KeyboardInterrupt()
		#sys.exit(1)
	return None, None
		
if __name__ == '__main__':
	while True:
		n = int(input("Enter numbers:"))
		
		start = time.time()
		res1, res2 = siqs_main(n)
		finish = time.time()
		cost = finish - start
		#print("Factors founded: ", res1, "("+ str(len(str(res1)))+"digits)")
		
		#print("Factors founded: ", res2, "("+ str(len(str(res2)))+"digits)")
		assert res1 * res2 == n
		
		print("cost =", cost)
		
		f = open("log/record.log", "a")

		print(datetime.now(), "number =", n, "("+ str(len(str(n))) +" digits)",
			"factor =", res1, "(" + str(len(str(res1))) + " digits) cost =", cost, file=f)
		
		f.close()



















