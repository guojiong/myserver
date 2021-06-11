from selenium import webdriver

from stock.models import Hq_history


def scrapy_stock_info(codes):
    url = 'http://quote.eastmoney.com/%s.html?from=BaiduAladdin'
    opt = webdriver.ChromeOptions()
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=opt)
    print('************* start *************')
    for c in codes:
        data = {}
        driver.get(url % c)
        print(c)
        element = driver.find_element_by_id('quote-digest')
        data['code'] = c
        data['date'] = driver.find_element_by_id('day')[1:11]
        data['sprice'] = element.find_element_by_id('gt1').text
        data['hprice'] = element.find_element_by_id('gt2').text
        data['eprice'] = driver.find_element_by_id('price9')
        data['lprice'] = element.find_element_by_id('gt9').text
        data['volume'] = element.find_element_by_id('gt5').text
        data['changeamount'] = driver.find_element_by_id('km1').text
        data['changerange'] = driver.find_element_by_id('km2').text
        data['p5'] = ''
        data['p10'] = ''
        data['p20'] = ''
        data['v5'] = ''
        data['v10'] = ''
        data['v20'] = ''
        data['hsl'] = element.find_element_by_id('gt4').text
        data['lb'] = element.find_element_by_id('gt11').text

        Hq_history.objects.update_or_create(defaults=data, )
