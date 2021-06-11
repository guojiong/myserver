import json

import numpy
import requests

# 代码获取sql  select * from
from stock.stock_sync import db_do_sql

'''SELECT a.code FROM (SELECT (t.nprice-t.startprice)/t.startprice as zf,t.* FROM `stockprice` t WHERE t.time>='14:30' 
AND t.time < '14:40' AND t.date = '2021-06-04' AND (t.nprice-t.startprice)/t.startprice >=0.03 
AND (t.nprice-t.startprice)/t.startprice <= 0.05) a GROUP BY a.time ORDER BY a.time desc
'''


def lb_hsl_run(l_codes):
    # codes = list()
    print(l_codes)

    for c in l_codes:
        url = 'http://qt.gtimg.cn/q=%s' % c

        sql = 'INSERT INTO `stock`.`lbhsl2`(`code`, `date`, `volume`, `turnoverrate`, `time`, `circulation`) VALUES %s'
        result = requests.get(url=url)
        l_result = result.text[12:-3].split('~')
        akdaily = l_result[38]
        data = (c, l_result[30][0:8], int(l_result[6])*100, l_result[38], l_result[30][-6:], l_result[-2])
        sql = sql % str(data)
        print(sql)
        db_do_sql(sql_script=sql)


# codes = ['sz000001', 'sz000068']
# lb_hsl_run(codes)
