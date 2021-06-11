import json
import requests
from stock.scrapy.stock_sync import db_do_sql

url = 'http://api.finance.ifeng.com/akdaily/?code=%s&type=last'
codes = db_do_sql(sql_script='select concat(origin,code) from stock.stock')
print(codes)
for code in codes:
    result = requests.get(url=url % code[0])
    print(result.text)
    data = json.loads(result.text)['record']
    sql = 'INSERT INTO `stock`.`qh_history`(`code`, `date`, `sprice`, `hprice`, `eprice`, `lprice`, `volume`, `changeamount`, `changerange`, `p5`, `p10`, `p20`, `v5`, `v10`, `v20`, `hsl`) VALUES '
    for d in data:
        # print(d)
        d[-2] = d[-2].replace(',', '')
        d[-3] = d[-3].replace(',', '')
        d[-4] = d[-4].replace(',', '')
        sql = sql + "('" + code[0] + "', '" + '\', \''.join(d) + '\'),'
    # print(data)
    # sql = sql % data
    db_do_sql(sql_script=sql[0:-1])
