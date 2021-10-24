# -*-coding:utf-8 -*-

"""
# File       : teat.py
# Time       ：2021/10/24 12:40
# Author     ：toby
# version    ：python 3.6
# Description：
"""
import datetime
import json
import os
import re
from pprint import pprint
import inquirer
from inquirer import errors
from prettytable import PrettyTable

'''
ditc_info规范
ditc_info={电话1 : [时间1,时间2,时间3······],
           电话2 : [时间1,时间2,时间3······],
           }
'''
#配置区
file='data.json' #json文件位置
def yesterday(in_date):

    dt = datetime.datetime.strptime(in_date, "%Y-%m-%d")
    out_date = (dt + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    return (out_date)


def nub_validation(answers, current): #输入学号是的判断
    if not re.match('[0-9]{10}', current):
        raise errors.ValidationError('', reason='请输入正确的11位电话号码')
    # elif not len(db.get_st(current))==0:
    #     raise errors.ValidationError('', reason='该学号已存在')
    return True

def add_lk_ditc(file,ditc_info):
    aa=open_lk_ditc(file)
    new_lk={}
    for i in ditc_info.keys():
        if i in aa:
            for ii in ditc_info[i]:
                t=-1
                for h in aa[i]:
                    if h['date']==ii['date'] and h['time']==ii['time']:
                        t=1
                if t==-1:
                    aa[i].append({'date': ii['date'], "time": ii['time']})
                    flog = -1
                    for day_dis in aa[i]:
                        if day_dis['date'] == yesterday(ii['date']):
                            flog = 1
                    if flog == -1:
                        new_lk[i] = ditc_info[i]
                else:
                    print("存在重复添加（同一人在同一时间登记）")
        else:
            aa[i]=ditc_info[i]
            new_lk[i]=ditc_info[i]
    with open(file,"w") as f:
        json.dump(aa, f, ensure_ascii=False)
    return new_lk
#把python对象转换为josn
def seve_lk_ditc(file,ditc_info):
    with open(file,"w") as f:
        json.dump(ditc_info,f,ensure_ascii=False)

# josn文件打开
def open_lk_ditc(file):
    with open(file,"r") as f:
        a=json.load(f)
    return a





if __name__ == '__main__':

    while 1:
        questions = [
            inquirer.List('size',
                          message="请选择功能",
                          choices=['[1]添加当天名单', '[2]手机号查询','[3]查看名单', '[4]重置'],
                          ),
        ]
        answers = inquirer.prompt(questions)


        if answers['size'] == '[4]重置':
            dict = {}
            str = '''
18877776666@2021-10-18 09:30:12
18855556666@2021-10-18 10:09:39
18844446666@2021-10-18 11:39:45
18833336666@2021-10-18 14:40:23
18822226666@2021-10-18 15:55:11
18877776666@2021-10-18 16:30:18'''
            for s in re.split('\n', str):
                if s != '':
                    number = re.split('@', s)[0]
                    date = re.split('@|\s', s)[1]
                    time = re.split('@|\s', s)[2]
                    if number in dict:
                        dict[number].append({'date': date, "time": time})
                    else:
                        dict[number] = [{'date': date, "time": time}, ]
            seve_lk_ditc(file, dict)
            os.system('cls')
            print("#---------重置成功-----------")

        elif answers['size'] == '[1]添加当天名单':
            os.system('cls')
            stopword = ''  # 修改输入终止符为#
            str = ''
            print('请输入内容【单独输入‘‘ 或连续两次回车保存退出】：')
            for line in iter(input, stopword):
                str += '\n'+line
            os.system('cls')
            # print(re.split('\n', str))
            dict = {}
            # print(type(dict))
            os.system('cls')

            for s in re.split('\n', str):
                if s != '':
                    number = re.split('@', s)[0]
                    date = re.split('@|\s', s)[1]
                    time = re.split('@|\s', s)[2]
                    if number in dict:
                        dict[number].append({'date': date, "time": time})
                    else:
                        dict[number] = [{'date': date, "time": time}, ]
                    # print(number, date, time)
            # pprint(dict)


            s = add_lk_ditc(file,dict)
            x = PrettyTable()
            x.field_names = ["新游客电话号码", "日期", "时间"]
            for i in s.keys():
                for ii in s[i]:
                    x.add_row([i, ii['date'], ii['time']])
            print(x)
            print("今天新用户人数：{0}人".format(len(s.keys())))
            input("按回车退出：")
            os.system('cls')

        elif answers['size'] == "[2]手机号查询":
            os.system('cls')
            questions = [
                inquirer.Text('nub',
                              message="请输入11位电话号码",
                              validate=nub_validation
                              ), ]
            answers = inquirer.prompt(questions)
            aa=open_lk_ditc(file)
            if answers['nub'] in aa:
                s=aa[answers['nub']]

                x = PrettyTable()
                x.field_names = ["电话号码", "日期", "时间"]
                for ii in s:
                    x.add_row([answers['nub'], ii['date'], ii['time']])

                print(x)
            else:
                print("没有查询到该号码")
            input("按回车退出：")
            os.system('cls')

        elif answers['size'] == '[3]查看名单':
            os.system('cls')
            s=(open_lk_ditc(file))
            x = PrettyTable()
            x.field_names = ["电话号码", "日期", "时间"]
            for i in s.keys():
                for ii in s[i]:
                    x.add_row([i, ii['date'], ii['time']])
                x.field_names = ["电话号码", "日期", "时间"]
            print(x)
            input("按回车退出：")
            os.system('cls')
            # pprint(open_lk_ditc(file))
        pass




