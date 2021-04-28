import time

from selenium.webdriver import Chrome
from chaojiying import  Chaojiying_Client
web=Chrome()

web.get('http://www.chaojiying.com/user/login/')

#处理验证码
img = web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/div/img').screenshot_as_png

chaojiying = Chaojiying_Client('123toby', '15924275250nn', '914981')
pic=chaojiying.PostPic(img, 1902)
print(pic['pic_str'])

time.sleep(2)
#登录
web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/p[1]/input').send_keys('123toby')
web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/p[2]/input').send_keys('15924275250nn')
web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/p[3]/input').send_keys(pic['pic_str'])
web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/p[4]/input').click()




