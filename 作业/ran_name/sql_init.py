# -*-coding:utf-8 -*-

"""
# File       : sql_init.py
# Time       ：2021/10/16 14:50
# Author     ：toby
# version    ：python 3.6
# Description：
"""
import sqlite3

f=open("student_2.sql","r",encoding="utf-8")
print(f.read())
cx = sqlite3.connect("test.db")
print(123)
cu = cx.cursor()
cu.executescript(f.read())
cx.commit()
cu.execute("select * from student_2" )
print(cu.fetchall())