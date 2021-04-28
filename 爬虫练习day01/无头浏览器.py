import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.support.select import Select


#准备配置无头浏览器参数
opt=Options()
opt.add_argument('--headless')
opt.add_argument('--disbale-gpu')


web=Chrome(options=opt) #载入设置参数


web.get("https://www.endata.com.cn/BoxOffice/BO/Year/")

#定位下拉框
sel_el=web.find_element_by_xpath('//*[@id="OptionDate"]')
#对元素进行包装，包装下拉框
sel=Select(sel_el)

#遍历选项
for i in range(len(sel.options)):
    time.sleep(2)
    #切换选项
    sel_text= sel.select_by_index(i)

    table=web.find_element_by_xpath('//*[@id="TableList"]/table').text
    # print(table)


    #拿页面代码（经过处理过的代码）
    print(web.page_source)



