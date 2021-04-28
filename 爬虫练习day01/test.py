import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


web = webdriver.Chrome()
web.get("https://lagou.com")


# web.maximize_window()


# #
# web.find_element_by_xpath('//*[@id="kw"]').send_keys('苹果2021发布会')
# web.find_element_by_xpath('//*[@id="su"]').click()
el=web.find_element_by_xpath('//*[@id="changeCityBox"]/p[1]/a')
el.click()  #点击全国

time.sleep(1)   #时间睡眠
web.find_element_by_xpath('//*[@id="search_input"]').send_keys('python',Keys.ENTER) #输入python 然后回车


#提取信息
li_list=web.find_elements_by_xpath('//*[@id="s_position_list"]/ul/li')

for li in li_list:
    job_nmae=li.find_element_by_tag_name('h3').text
    job_nmae2=li.find_element_by_class_name('add').text
    job_money=li.find_element_by_class_name('money').text

    print(job_nmae+job_nmae2+'  '+job_money)


time.sleep(3)
#窗口跳转
web.find_element_by_xpath('//*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[1]/a/h3').click()

#注意selenium 默认不会自动切换窗口
web.switch_to.window(web.window_handles[-1])

#获取信息
job_detail=web.find_element_by_xpath('//*[@id="job_detail"]/dd[2]').text
print(job_detail)

time.sleep(1)
#关闭窗口
web.close()

time.sleep(1)
web.switch_to.window(web.window_handles[0])
print(web.find_element_by_xpath('//*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[1]/a/h3').text)


# #处理iframe
# iframe=web.find_element_by_xpath('####')
# web.switch_to.frame(iframe)
#
# #切换回原页面
# web.switch_to.default_content()





print(web.title)

print('======回车关闭浏览器====')
a=input()
time.sleep(1)
web.refresh()
web.close()


