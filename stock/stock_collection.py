from time import sleep
from selenium import webdriver

from stock.stock_sync import db_do_sql

flag = 'sh'
if flag == 'sh':
    url = 'http://quote.eastmoney.com/center/gridlist.html#sh_a_board'
else:
    url = 'http://quote.eastmoney.com/center/gridlist.html#sz_a_board'

#  创建配置对象
opt = webdriver.ChromeOptions()

#  添加配置参数
opt.add_argument('--headless')
opt.add_argument('--disable-gpu')

#  创建浏览器对象的时候添加配置对象
driver = webdriver.Chrome(chrome_options=opt)
driver.get(url)

paginate = driver.find_element_by_id('main-table_paginate')
counts_tab = paginate.find_element_by_xpath('./span/a[last()]').text

for i in range(2, int(counts_tab) + 2):
    stocks = list()
    next_page = ''
    sleep(2)
    element = driver.find_element_by_id('table_wrapper-table')
    als = element.find_elements_by_xpath('./tbody/tr')
    for t in als:
        stock = '(\''
        a = t.find_elements_by_xpath('.//a')
        stock = stock + a[0].text + '\', \''
        stock = stock + a[1].text + '\', \''
        stock = stock + url.split('#')[1][0:2] + '\')'
        stocks.append(stock)
    data = ', '.join(stocks)
    sql = 'insert into stock.stock (code, name, origin) values %s' % data
    db_do_sql(sql_script=sql)
    print('第%s页' % i)
    next_page = paginate.find_elements_by_xpath('./a')[1]
    next_page.click()
