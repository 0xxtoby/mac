# -*-coding:utf-8 -*-

"""
# File       : 123.py
# Time       ：2021/10/16 14:35
# Author     ：toby
# version    ：python 3.6
# Description：
"""
import os
import random
import re
import inquirer
import sqlite3
from inquirer import errors


# 配置文件区
db_tables_name="student_2_copy1"
db_file="test.db"


class db_util:     #SQLlit 相关操作

    def get_len(self):
        cx = sqlite3.connect(db_file)
        cu = cx.cursor()
        cu.execute("select * from {0}".format(db_tables_name))
        return len(cu.fetchall())
    def get_student_dis(self):
        cx = sqlite3.connect(db_file)
        cu = cx.cursor()
        cu.execute("select * from {0}".format(db_tables_name))
        return cu.fetchall()
    def del_st(self,no):
        cx = sqlite3.connect(db_file)
        cu = cx.cursor()
        cu.execute("delete from {0} where No = {1}".format(db_tables_name,no))
        cx.commit()
    def modify_st(self,id,nub,name):
        cx = sqlite3.connect(db_file)
        cu = cx.cursor()
        cu.execute("update {0} set name=\"{1}\",number={2} where No = {3}".format(db_tables_name,name,nub,id))
        cx.commit()
    def get_st(self,nub):
        cx = sqlite3.connect(db_file)
        cu = cx.cursor()
        cu.execute("select * from {0} where number={1}".format(db_tables_name,nub))
        return cu.fetchall()

db=db_util()

def printf_st(data):    #格式化输出选中学生名单
    print("#########随机点名##########")
    print("   序号    学号   姓名")
    for a in data:

        if a[0]<10:
            print("   "+"0"+str(a[0]) + "-" + str(a[1]) + "-" + a[2])
        else:
            print("   "+str(a[0])+"-"+str(a[1])+"-"+a[2])
    print("###########################")

def format_dis(data):  #格式化输出名单
    ss=[]
    for a in data:
        if a[0]<10:
            a0="0"+str(a[0])
        else:
            a0=str(a[0])
        if len(a[2])==2:
            a2=a[2][0]+"  "+a[2][1]
        else:
            a2=a[2]
        ss.append(a0+'-'+str(a[1])+'-'+a2)
    return ss


def ran_data():  #主函数 从数据库中读取后随机抽取一名学生
    st_no=random.randint(1, db.get_len())#随机到的学生序号
    student_dis=db.get_student_dis()[st_no-1]
    return student_dis
# def add_st(sumber,name):


def nub_validation(answers, current): #输入学号是的判断
    if not re.match('[0-9]{10}', current):
        raise errors.ValidationError('', reason='请输入正确的10位学号')
    elif not len(db.get_st(current))==0:
        raise errors.ValidationError('', reason='该学号已存在')

    return True

if __name__ == '__main__':
    data=[]
    while 1:
        questions = [
          inquirer.List('size',
                        message="请选择功能",
                        choices=['[1]随机点名', '[2]学生名单管理'],
                    ),
        ]
        answers = inquirer.prompt(questions)

        os.system('cls')
        if answers['size']=='[1]随机点名':
            while 1:
                questions = [
                    inquirer.List('size',
                                  message="请选择功能",
                                  choices=['[1]自动点名', '[2]清空', '[3]退出'],

                                  ),
                ]
                data.append(ran_data())
                answers = inquirer.prompt(questions)
                if answers["size"]=='[2]清空':
                    data=[]
                    os.system('cls')
                    continue
                elif answers["size"]=='[3]退出':
                    os.system('cls')
                    break

                os.system('cls')
                printf_st(data)



        elif answers['size']=='[2]学生名单管理':
            while 1:
                questions = [
                    inquirer.List('ck',
                                  message="选择学生查看详细",
                                  choices=format_dis(db.get_student_dis()),
                                  ),
                ]
                answers = inquirer.prompt(questions)
                os.system('cls')

                no = re.split("-", answers["ck"])[0]
                nub= re.split("-", answers["ck"])[1]
                name = re.split("-", answers["ck"])[2]
                print("###########学生信息############\n     id  ：{0}\n     学号：{1}\n     姓名：{2}".format(no,nub,name))
                questions = [
                    inquirer.List('ck',
                                  message="功能选择",
                                  choices=['[1]删除', '[2]修改', '[3]退出'],
                                  ),
                ]
                answers = inquirer.prompt(questions)
                if answers["ck"]=='[1]删除':

                    db.del_st(no=no)
                    os.system('cls')
                    print("########"+name+' 删除成功'
                                          +"########")
                elif answers["ck"]=='[2]修改':
                    os.system('cls')
                    print("###########修改学生信息############\n     id  ：{0}\n     学号：{1}\n     姓名：{2}".format(no, nub, name))
                    questions = [
                        inquirer.Text('name', message="请输入修改后姓名"),
                        inquirer.Text('nub',
                                      message="请输入修改后学号",
                                      validate=nub_validation
                                      ), ]

                    answers = inquirer.prompt(questions)
                    os.system('cls')
                    db.modify_st(id=no,nub=answers['nub'],name=answers['name'])
                    print("#######"+answers['name']+"修改成功########")
                else:
                    os.system('cls')
                    break
