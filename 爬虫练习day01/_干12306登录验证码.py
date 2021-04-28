import time

from selenium.webdriver.chrome.options import Options

from chaojiying import  Chaojiying_Client
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains

#========隐藏selenium标识=======
opt=Options()
opt.add_argument('--disable-blink-features=AutomationControlled')
web=Chrome(options=opt)
#===================

web.get('https://kyfw.12306.cn/otn/resources/login.html')

time.sleep(2)
web.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]/a').click()

time.sleep(3)

#获取验证码
verify_img=web.find_element_by_xpath('//*[@id="J-loginImg"]')

chaojiying = Chaojiying_Client('123toby', '15924275250nn', '914981')
dic=chaojiying.PostPic(verify_img.screenshot_as_png, 9004) #x1,y1|x2,y2|x3,y3
result=dic['pic_str']
print(result)
rs_list=result.split("|")
#点击验证码
for rs in rs_list:# x1,y1
    bb=rs.split(",")
    x=int(bb[0])
    y=int(bb[1])
    ActionChains(web).move_to_element_with_offset(verify_img,x,y).click().perform()#定义事件


#输入账号密码
web.find_element_by_xpath('//*[@id="J-userName"]').send_keys('18395927141')
web.find_element_by_xpath('//*[@id="J-password"]').send_keys('15924275250nn')
web.find_element_by_xpath('//*[@id="J-login"]').click()

time.sleep(5)
huakuai=web.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span')
ActionChains(web).drag_and_drop_by_offset(huakuai,300,0).perform()





