try:
    num1=input('yi:')
    num2=input('er')
    print('结果%d'%(int(num1)/int(num2)))
except ZeroDivisionError:
    print('第二个数字buwei0')
except:
    print("buhuoyican")
else:
    print("计算正常")
finally:
    print("sususuus")
