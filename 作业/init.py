# import sqlite3
# cx = sqlite3.connect("test.db")
# cu = cx.cursor()
#
# cu.execute("select * from student")
# print(len(cu.fetchall()))


a=[(2, 1962120007, '陈禹良', None), (24, 1962120127, '贺泽龙', None), (5, 1962120033, '张雲峰', None), (30, 1965130033, '卢思宇', None), (7, 1962120039,
'王学鹏', None), (19, 1962120106, '毛宇杰', None), (6, 1962120036, '王路平', None), (22, 1962120114, '王姝婧', None), (25, 1962150038, '赵奕骏', None),
 (18, 1962120103, '陈凯', None), (20, 1962120111, '陈思滔', None), (29, 1965110108, '柳洲洋', None), (12, 1962120071, '吴万隆', None)]

def printf_st(data):
    print("##########################")
    print("   序号    学号    姓名")
    for a in data:

        if a[0]<10:
            print("   "+"0"+str(a[0]) + "-" + str(a[1]) + "-" + a[2])
        else:
            print("   "+str(a[0])+"-"+str(a[1])+"-"+a[2])
    print("##########################")

printf_st(a)