import pyfactor
from pyfactor.rho import brent
from pyfactor.siqs import siqs_main as siqs
from pyfactor.ecm import parallel_ecm as ecm
from pyfactor.pm1 import pm1
from pyfactor.pp1 import pp1

import sys
import math

from random import randint

try:
	import sympy
	from sympy import isprime
except ImportError:
	print("请安装SymPy Library!")
	sys.exit(1)

VERSION = "0.1"
MAX_DIGITS = 60

#=================================
#	字典操作
#=================================
def add_factors(p, factors, value=1):
	if factors.get(p) is None:
		factors[p] = value
	else:
		factors[p] += value

#=================================
#	试除法
#=================================
def trial_divison(n, B=10**6, factors={}):
	'''
	输入:
		n: 带分解的整数
		B: 素数表的上界
		factors: n的所有素因子组成的字典，
				 key为素因子，value为素因子的个数
	输出:
		rem: 还没有分解的部分
	'''
	rem = n
	for p in sympy.sieve.primerange(2, B):
		exp = 0
		while rem % p == 0:
			rem //= p
			exp += 1
		if exp > 0:
			add_factors(p, factors, exp)
	return rem
	
#======================================
#	是否为素数的方幂
#======================================
def is_power(n, B=10**6+3):
	exp = math.ceil(math.log(n, B))
	for e in range(exp, 2, -1):
		p, flag = sympy.integer_nthroot(n, e)
		if flag:
			return p, e
	return None, None


#=====================================
#	整数分解
#=====================================
def factor(n, factors={}, partial={}, times=1, options=[10**6, 10**5, 10**6, 20]):

	# 1. 素性判别
	if isprime(n):
		add_factors(n, factors, times)
		return
		
	# 2. 试除法
	n_tmp = n
	print("Trial Division...")
	n = trial_divison(n, factors=factors)
	if n < n_tmp:
		print("Find factor:", n_tmp // n)
	
	if n == 1:
		return
	elif isprime(n):
		add_factors(n, factors, times)
		return
	
	# 3. brent方法
	print("Using Brent Method...")
	for c in range(1, 4):
		print("poly: x^2 +", c)
		f = brent(n, c=c, limit=options[0])
		if f is not None:
			n //= f
			if isprime(f):
				print("Find prime: ", f)
				add_factors(f, factors, times)
			else:
				print("Find coprime factor: ", f)
				add_factors(f, partial, times)
	
	if isprime(n):
		add_factors(n, factors, times)
		return

	# 4. pp1方法
	print("Using Williams p + 1 Method...")
	f = pp1(n, B=options[1], r=3, retries=3)
	if f is not None:
		n //= f
		if isprime(f):
			print("Find prime: ", f)
			add_factors(f, factors, times)
		else:
			print("Find coprime factor: ", f)
			add_factors(f, partial, times)
	
		if isprime(n):
			add_factors(n, factors, times)
			return
	
	# 5. pm1方法
	seed = randint(2, 10)
	print("Using Pollard's p - 1 Method...")
	f = pm1(n, B=options[2], r=seed)
	if f is not None:
		n //= f
		if isprime(f):
			print("Find prime: ", f)
			add_factors(f, factors, times)
		else:
			print("Find coprime factor: ", f)
			add_factors(f, partial, times)
	
		if isprime(n):
			add_factors(n, factors, times)
			return
			
	# 6. ECM 方法
	print("Using ECM Method...")
	while True:
		old_len = len(str(n))
		f = ecm(n, verbose=False, digits=options[3], limits=15)
		if f is not None:
			n //= f
			if isprime(f):
				print("Find prime: ", f)
				add_factors(f, factors, times)
			else:
				print("Find coprime factor: ", f)
				add_factors(f, partial, times)

			if isprime(n):
				add_factors(n, factors, times)
				return
		
		if old_len == len(str(n)) or len(str(n)) < 45:
			break

	# 是否为方幂
	p, e = is_power(n)
	if p is not None:
		if isprime(p):
			add_factors(p, factors, e*times)
		else:
			add_factors(f, partial, e*times)
		return

	if len(str(n)) <= MAX_DIGITS:
		# 7. SIQS方法
		print("Using SIQS Method")
		f1, f2 = siqs(n)
		if f1 is not None:
			n = 1
			if isprime(f1):
				print("Find prime: ", f1)
				add_factors(f1, factors, times)
			else:
				print("Find coprime factor: ", f1)
				add_factors(f1, partial, times)
			
			if isprime(f2):
				print("Finding prime: ", f2)
				add_factors(f2, factors, times)
			else:
				print("Finding coprime factor: ", f2)
				add_factors(f2, partial, times)
		
	if n > 1:
		add_factors(n, partial, times)
		return
	

def main(n, options=[10**6, 10**5, 10**6, 23]):
	# 完全分解的部分
	factors = {}
	# 没有完全分解的部分
	partial = {}
	
	unknown = {}
	
	dn = len(str(n))
	try:
		factor(n, factors=factors, partial=partial, options=options)
		while partial != {}:
			tmp = partial
			partial = {}
			for p, e in tmp.items():
				if len(str(p)) > MAX_DIGITS:
					add_factors(p, unknown, e)
					continue
				factor(p, factors, partial, e, options)
	except KeyboardInterrupt:
		for p, e in factors.items():
			n //= p**e
		add_factors(n, unknown)
	return factors, unknown


def command_line(n, options=[10**6, 10**5, 10**6, 23]):
	dn = len(str(n))
	print("正在分解", n, "("+str(dn)+" 位)")
	
	factors, unknown = main(n, options)
	
	print("\n"+str(n)+"分解结果如下:")
	for p, e in factors.items():
		if p < n:
			dp = len(str(p))
			if e == 1:
				print("    素因子: p"+str(dp)+" =", p)
			elif e > 1:
				print("素数幂因子: 底数 p"+str(dp)+" =", p, "指数 =", e)
		else:
			print(str(n)+"为素数")
	
	if unknown != {}:
		
		for c, e in unknown.items():
			if c == n:
				print(str(n)+"没有被完全分解")
			else:
				dc = len(str(c))
				if e == 1:
					print("  合数因子: c"+str(dc)+" =", c)
				elif e > 1:
					print("合数幂因子: 底数c"+str(dc)+" =", c, "指数 =", e)
					
					
def interative(argv=[]):
	n = 1
	options=[10**6, 10**5, 10**6, 23]
	
	if len(argv) > 1:
		for item in argv[1:]:
			if item == "-h":
				help()
				sys.exit()
			elif item == '-v':
				show_version()
				sys.exit()
			elif item[:6] == "--rho=":
				options[0] = int(item[6:])
			elif item[:6] == "--pp1=":
				options[1] = int(item[6:])
			elif item[:6] == "--pm1=":
				options[2] = int(item[6:])
			elif item[:6] == "--ecm=":
				options[3] = int(item[6:])	
			else:
				try:
					n = eval(item)
				except:
					continue
	if n > 1:
		command_line(n, options=options)
	else:
		print("pyfactor %s 基于python的整数分解工具" % VERSION)
		print("输入 \"exit\" 或 \"quit\" 退出；输入\"?\"或\"help\"显示帮助")
		while True:
			recived = input("\n>>> ")
			if recived == "quit" or recived == "exit":
				break
			elif recived == "?" or recived == "help":
				help()
				continue
			else:
				try:
					n = eval(recived)
				except:
					print("未知表达式")
					continue
			if n <= 1 or type(n) is not int:
				print("请输入大于1的正整数")
				continue
			command_line(n, options=options)

def help():
   print( '''\
用法: pyfactor_cli.py [选项] [表达式]
基于python的整数分解工具

-h			显示帮助信息
-v			显示版本信息
--rho=n		Pollard's rho方法的迭代次数限制为 n 次 	 
--pp1=B		Williams p+1方法的光滑界设置为 B
--pm1=B		Pollard's p-1方法的光滑界设置为 B
--ecm=d		ECM方法寻找的素因子大小限制为十进制 d 位

使用过程中发现Bug，请联系<1368753673@qq.com> 
感谢使用!''')
   #sys.exit()
 
def show_version():
	print('''\
pyfactor version %s 基于python的整数分解工具''' % VERSION)
	#sys.exit()
   
 
if __name__ == '__main__':
	interative(sys.argv)
	
	
	
	
	