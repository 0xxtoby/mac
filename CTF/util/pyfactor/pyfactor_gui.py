
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu, Message
from tkinter import Spinbox, Toplevel
from tkinter import messagebox as mBox

import pyfactor
from pyfactor.rho import brent
from pyfactor.siqs import siqs_main as siqs
from pyfactor.ecm import parallel_ecm as ecm
from pyfactor.pm1 import pm1
from pyfactor.pp1 import pp1

import sys
import math
import time

from random import randint

import threading

try:
	import sympy
	from sympy import isprime, nextprime
except ImportError:
	print("请安装SymPy Library!")
	sys.exit(1)

VERSION = "0.1"

###################################################
#	
#	回调函数定义
#
###################################################


def thread_it(func):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func) 
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()

#================================
#	关于信息
#================================
def _msgBox():
    mBox.showinfo('pyfactor整数分解工具', 
            "pyfactor version %s \n基于python的整数分解工具\n使用过程中发现Bug，请联系\n"
			"<1368753673@qq.com> "

			"感谢使用!" % VERSION)
#================================
#  退出
#================================
def _quit():
    win.quit()
    win.destroy()
    exit()


win = tk.Tk()
win.title("pyfactor整数分解工具")

tabControl = ttk.Notebook(win)

tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='整数分解')

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='素数生成与检验')

tabControl.pack(expand=1, fill="both")

###################################################################
#
#	整数分解部分
#
###################################################################
# 菜单设置
menuBar = Menu(win)
win.config(menu=menuBar)

helpMenu = Menu(menuBar, tearoff=0)
helpMenu.add_command(label="关于", command=_msgBox)
helpMenu.add_separator()
helpMenu.add_command(label="退出", command=_quit)
menuBar.add_cascade(label="选项", menu=helpMenu)

# 算法选择区
ttk.Label(tab1, text="方法选择:").grid(column=0, row=0)

factor_method = tk.StringVar()
methodChosen = ttk.Combobox(tab1, width=20, textvariable=factor_method, state='readonly')
methodChosen['values'] = ("Brent方法", "p+1方法", "p-1方法", "ECM方法", "SIQS方法")
methodChosen.grid(column=0, row=1)
methodChosen.set("请选择")

# 算法运行区
monty = ttk.LabelFrame(tab1, text=factor_method.get(), labelanchor="n")
monty.grid(column=0, row=2, padx=80, pady=4)

result = ttk.LabelFrame(tab1, text=factor_method.get(), labelanchor="n")
result.grid(column=0, row=3, padx=80, pady=4)
result.configure(text='运行结果')

scrolW = 50
scrolH = 10
scr = scrolledtext.ScrolledText(result, width=scrolW, height=scrolH, wrap=tk.WORD)
scr.grid(column=0, row=1, columnspan=3)


prog = ttk.Progressbar(result, mode='indeterminate')
prog.grid(column=0, row=0, columnspan=3)
prog.grid_forget()

widget_list = []



def _run():
	prog.grid(column=0, row=0, columnspan=3)
	scr.delete(1.0, 'end')
	
	n = eval(number.get())
	a = seed.get()
	c = cof.get()
	li = limit.get()
	B = smooth_bound.get()
	d = digits.get()
	method_name = factor_method.get()
	
	if method_name == "Brent方法":
		scr.insert(tk.INSERT, 'Pollard rho方法:\n')
		scr.insert(tk.INSERT, '正在寻找'+ str(n) +'('+str(len(str(n)))+'位)的因子，请耐心等待......\n\n')
		start = time.time()
		g = brent(int(n), r=int(a), c=int(c), limit=int(li))
		finish = time.time()
		cost = finish - start
		if g is not None:
			scr.insert(tk.INSERT, '找到因子: '+str(g)+' ('+str(len(str(g)))+'位)\n\n')
		else:
			scr.insert(tk.INSERT, '算法运行失败，请重选参数！\n\n')
		scr.insert(tk.INSERT, '运行时间: '+str(cost)+'s\n')
		prog.grid_forget()
		
	elif method_name == "p+1方法":
		scr.insert(tk.INSERT, 'Williams p+1方法:\n')
		scr.insert(tk.INSERT, '正在寻找'+ str(n) +'('+str(len(str(n)))+'位)的因子，请耐心等待......\n\n')
		start = time.time()
		g = pp1(int(n), B=int(B), r=int(a), retries=1)
		finish = time.time()
		cost = finish - start
		if g is not None:
			scr.insert(tk.INSERT, '找到因子: '+str(g)+' ('+str(len(str(g)))+'位)\n\n')
		else:
			scr.insert(tk.INSERT, '算法运行失败，请重选参数！\n\n')
		scr.insert(tk.INSERT, '运行时间: '+str(cost)+'s\n')
		prog.grid_forget()
		
	elif method_name == "p-1方法":
		scr.insert(tk.INSERT, 'Pollard p-1方法:\n')
		scr.insert(tk.INSERT, '正在寻找'+ str(n) +'('+str(len(str(n)))+'位)的因子，请耐心等待......\n\n')
		start = time.time()
		g = pm1(int(n), B=int(B), r=int(a))
		finish = time.time()
		cost = finish - start
		if g is not None:
			scr.insert(tk.INSERT, '找到因子: '+str(g)+' ('+str(len(str(g)))+'位)\n\n')
		else:
			scr.insert(tk.INSERT, '算法运行失败，请重选参数！\n\n')
		scr.insert(tk.INSERT, '运行时间: '+str(cost)+'s\n')
		prog.grid_forget()
			
	elif method_name == "ECM方法":
		prog["mode"] = "indeterminate"
		prog.start(10)
		scr.insert(tk.INSERT, 'ECM方法:\n')
		scr.insert(tk.INSERT, '正在寻找'+ str(n) +'('+str(len(str(n)))+'位)的因子，请耐心等待......\n\n')
		start = time.time()
		g = ecm(int(n), verbose=True, digits=int(d))
		finish = time.time()
		cost = finish - start
		if g is not None:
			scr.insert(tk.INSERT, '找到因子: '+str(g)+' ('+str(len(str(g)))+'位)\n\n')
		else:
			scr.insert(tk.INSERT, '算法运行失败，请重选参数！\n\n')
		scr.insert(tk.INSERT, '运行时间: '+str(cost)+'s\n')
		prog.grid_forget()
		
	elif method_name == "SIQS方法":
		prog["mode"] = "determinate"
		scr.insert(tk.INSERT, 'SIQS方法:\n')
		scr.insert(tk.INSERT, '正在寻找'+ str(n) +'('+str(len(str(n)))+'位)的因子，请耐心等待......\n\n')
		start = time.time()
		f1, f2 = siqs(int(n), store=True, gui_prog=prog)
		finish = time.time()
		cost = finish - start
		if f1 is not None:
			scr.insert(tk.INSERT, '找到因子: '+str(f1)+' ('+str(len(str(f1)))+'位)\n\n')
			scr.insert(tk.INSERT, '找到因子: '+str(f2)+' ('+str(len(str(f2)))+'位)\n\n')
		else:
			scr.insert(tk.INSERT, '算法运行失败，请重选参数！\n\n')
		scr.insert(tk.INSERT, '运行时间: '+str(cost)+'s\n')
		prog.grid_forget()


seed = tk.StringVar() 		  	# 初始值
cof = tk.StringVar()			# 多项式参数
limit = tk.StringVar()  		# Brent方法迭代次数限制
smooth_bound = tk.StringVar() 	# 光滑界
digits = tk.StringVar()
number = tk.StringVar()

def _change(*args):
			
	while widget_list:
		w = widget_list.pop()
		w.destroy()
	method_name = factor_method.get()
	monty.configure(text=factor_method.get())
	
	r = 0
	
	# Brent方法
	if method_name == "Brent方法":
		# 初始值
		a_label = ttk.Label(monty, width=0,text="初始值:")
		widget_list.append(a_label)
		a_label.grid(column=0, row=r)
		
		seedInput = ttk.Entry(monty, width=5, textvariable=seed)
		widget_list.append(seedInput)
		seedInput.grid(column=1, row=r)
		
		
		# 多项式选择
		r += 1
		ploy_label = ttk.Label(monty,text="多项式x^2+c, c=")
		widget_list.append(ploy_label)
		ploy_label.grid(column=0, row=r)
		
		cofInput = ttk.Entry(monty, width=5, textvariable=cof)
		widget_list.append(cofInput)
		cofInput.grid(column=1, row=r)
		
		# 迭代次数限制
		r += 1
		brent_limit_label = ttk.Label(monty, text="最大迭代次数:")
		widget_list.append(brent_limit_label)
		brent_limit_label.grid(column=0, row=r)
		
		limitInput = ttk.Entry(monty, width=15, textvariable=limit)
		widget_list.append(limitInput)
		limitInput.grid(column=1, row=r)
		
	# p+1方法 与 p-1方法
	elif method_name == "p-1方法" or method_name == "p+1方法":
		# 初始值
		a_label = ttk.Label(monty, width=0,text="初始值:")
		widget_list.append(a_label)
		a_label.grid(column=0, row=r)
		
		seedInput = ttk.Entry(monty, width=5, textvariable=seed)
		widget_list.append(seedInput)
		seedInput.grid(column=1, row=r)
		# 光滑界
		r += 1
		bound_label = ttk.Label(monty, text="光滑界B1:")
		widget_list.append(bound_label)
		bound_label.grid(column=0, row=r)
		
		smoothInput = ttk.Entry(monty, width=15, textvariable=smooth_bound)
		widget_list.append(smoothInput)
		smoothInput.grid(column=1, row=r)
	
	# ECM
	elif method_name == "ECM方法":
		# 素因子大小
		bound_label = ttk.Label(monty, text="素因子大小:")
		widget_list.append(bound_label)
		bound_label.grid(column=0, row=r)
		
		digitsChosen = ttk.Combobox(monty, width=10, textvariable=digits, state='readonly')
		widget_list.append(digitsChosen)
		digitsChosen['values'] = list(range(12, 31, 1))
		digitsChosen.grid(column=1, row=r)
	
	# SIQS
	elif method_name == "SIQS方法":
		print("SIQS")
		
	r += 1
	numberInput = ttk.Entry(monty, width=50, textvariable=number, justify="right")
	widget_list.append(numberInput)
	numberInput.grid(column=0, row=r, columnspan=2)

	action = ttk.Button(monty, text="运行",command=lambda :thread_it(_run))
	widget_list.append(action)
	action.grid(column=2, row=r)
		
methodChosen.bind("<<ComboboxSelected>>", _change)

###################################################################
#
#	素数生成与检验部分
#
###################################################################

prime_size = tk.StringVar()
input_number = tk.StringVar()

def _genprime():
	prime_scr.delete(1.0, 'end')
	d = int(prime_size.get())
	p = nextprime(randint(10**(d-1), 10**d))
	prime_scr.insert(tk.INSERT, str(p))

def _checkprime():
	p = int(input_number.get())
	if isprime(p):
		mBox.showinfo('素性检验', str(p)+'是素数！')
	else:
		mBox.showerror('素性检验',str(p)+'不是素数！')
	

#========================================
#	素数生成区域
#========================================
gen_prime_area = ttk.LabelFrame(tab2, text="素数生成", labelanchor="n")
gen_prime_area.grid(column=1, row=0, padx=8, pady=4)

ttk.Label(gen_prime_area, text="素数规模（十进制位数）").grid(column=0, row=0)
ttk.Entry(gen_prime_area, width=5, textvariable=prime_size, justify="right").grid(column=1, row=0)

ttk.Button(gen_prime_area, text="生成", command=lambda :thread_it(_genprime)).grid(column=2, row=0)

ttk.Label(gen_prime_area, text="生成素数").grid(column=0, row=1)
prime_scr = scrolledtext.ScrolledText(gen_prime_area, width=20, height=10, wrap=tk.WORD)
prime_scr.grid(column=0, row=3, columnspan=3)

#========================================
#	素性检验区域
#========================================
isprime_area = ttk.LabelFrame(tab2, text="素性检验", labelanchor="n")
isprime_area.grid(column=0, row=0, padx=8, pady=4)

ttk.Label(isprime_area, text="输入待检验的整数）").grid(column=0, row=7)
ttk.Entry(isprime_area, width=30, textvariable=input_number, justify="right").grid(column=0, row=8)

ttk.Button(isprime_area, text="检验", command=lambda :thread_it(_checkprime)).grid(column=0, row=9)

win.mainloop()
