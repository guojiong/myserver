import datetime
import time
from time import sleep
import numpy
import pymysql
import requests

dict_names = ('code', 'name', 'startprice', 'yprice', 'nprice', 'hprice', 'lprice', 'bidingprice', 'auctionprice',
              'tradingvolume', 'tradingprice', 'buy1', 'buy1price1', 'buy2', 'buy2price', 'buy3', 'buy3price',
              'buy4', 'buy4price', 'buy5', 'buy5price', 'sale1', 'sale1price', 'sale2', 'sale2price', 'sale3',
              'sale3price', 'sale4', 'sale4price', 'sale5', 'sale5price', 'date', 'time', 'status')
url = 'http://hq.sinajs.cn/list=%s'
db_attr = ('localhost', '3306', 'root', '123456')


# db_attr = ('192.168.10.102', '3306', 'root', '123456')


def get_connect():
    return pymysql.connect(host=db_attr[0], port=int(db_attr[1]), user=db_attr[2], passwd=db_attr[3])


def stock_sync(codes):
    am_start_time = '09:29:00'
    am_end_time = '11:31:00'
    pm_start_time = '12:59:00'
    pm_end_time = '16:20:00'
    while True:
        hour = datetime.datetime.now().strftime('%H:%M:%S')
        codes_arr = numpy.array_split(codes, 10)
        if (am_start_time <= hour <= am_end_time) or (pm_start_time <= hour <= pm_end_time):
            for arr in codes_arr:
                sql = 'insert into stock.stockprice (%s) values ' % ', '.join(dict_names)
                try:
                    result = requests.get(url=url % ','.join(arr))
                    print(url % ','.join(arr))
                    result_list = result.text.split(';')
                    i = 0
                    for code in arr:
                        sql = sql + '("' + code + '", "' + '", "'.join(
                            result_list[i].split('=')[1][1:-3].split(',')[0:33]) + '"),'
                        i = i + 1
                    # print(sql[0:-1])
                    db_do_sql(sql[0:-1])
                except Exception as e:
                    print(e)
                    continue
        else:
            if hour > '15:00:00' and (int(hour[0:2]) - 9) >= 1:
                sleep(32000)
            elif hour < '09:00:00':
                sleep(1800)

        sleep(60)


# 连接数据库并执行sql, 连接重试3次
# 执行sql语句：sql_script
# 数据库连接信息：link
def db_do_sql(sql_script):
    # dbtype = link['dbtype']  # 数据库类型：dbtype
    # 数据库修改操作
    try:
        _conn_status = True
        _max_retries_count = 2  # 设置最大重试次数
        _conn_retries_count = 0  # 初始重试次数
        _conn_timeout = 10  # 连接超时时间为3秒
        conn = ''
        while _conn_status and _conn_retries_count <= _max_retries_count:
            try:
                conn = get_connect()
                # msql = pymysql.connect(host=sql_url, port=sql_port, user=sql_user, password=sql_password,
                #                        connect_timeout=_conn_timeout)
                _conn_status = False  # 如果conn成功则_status为设置为False则退出循环，返回db连接对象
            except Exception:
                _conn_retries_count += 1
                print(
                    '第%s次，连接数据库失败,数据库：%s' % (_conn_retries_count, db_attr))
                time.sleep(3)
        else:
            # logs.debugInfo('数据库地址：%s：%s，连接数据库成功!'% (sql_url,str(sql_port)))
            sql_cursor = conn.cursor()
            sql_cursor.execute(sql_script)
            if sql_script.strip()[0:6].lower() == 'select':
                req_data = sql_cursor.fetchall()
                conn.close()
                return req_data
            else:
                conn.commit()
                conn.close()
                return True
    except BaseException as error:
        print('数据执行 %s 操作异常，错误提示：%s' % (sql_script, str(error)))
        return False


def run():
    l_sql = 'select CONCAT(t.origin, t.`code`) from stock.stock t'
    l_codes = db_do_sql(sql_script=l_sql)
    # ['603511', '688510', '688315', '688068', '688316', '688097', '688005', '688050', '688613', '688630', '688056',
    #       '688026', '688317', '688559', '688551', '688408', '688233', '688665', '688468', '688388']
    # 多线程

    a_codes = list()
    for c in l_codes:
        a_codes.append(c[0])
    print(a_codes)
    stock_sync(a_codes)
# url = 'http://hq.sinajs.cn/list=%s' % ','.join(codes)
# print(url)
# requests.get(url=url)
