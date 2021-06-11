import datetime
import json
from time import sleep

import requests
from django.core import serializers
from django.db.models import Max, Count, F
from django.http import JsonResponse
from django.shortcuts import render
import threading
from stock.dao.query import q_stock, q_collectorstatus
from stock.lb_hsl_sync import lb_hsl_run
from stock.models import Stock, CollectorStatus, LbHsl, LbHsl2
from stock.stock_sync import run, stop_thread, db_do_sql


def index(request):
    return render(request, 'index.html')


def query_stock(request):
    code = request.POST.get('code')
    name = request.POST.get('name')
    origin = request.POST.get('origin')
    remark = request.POST.get('remark')
    result = q_stock(code, name, origin, remark)
    return JsonResponse({'status': 200, 'result': result})


def update_or_create(request):
    code = request.POST.get('code')
    name = request.POST.get('name')
    origin = request.POST.get('origin')
    remark = request.POST.get('remark')
    Stock.objects.update_or_create(defaults={'code': code, 'name': name, 'origin': origin, 'remark': remark}, code=code)
    return JsonResponse({'status': 200})


def upload_file(request):
    file = request.files.get('file')


def stock_sync(request):
    action = request.GET.get('action')
    cs = q_collectorstatus()
    try:
        if len(json.loads(cs)) == 0 and action == 'start':
            l_stocks = list()
            stock_list = json.loads(q_stock())
            for s in stock_list:
                st = s['fields']['origin'] + s['fields']['code']
                l_stocks.append(st)
            print(l_stocks)
            t = threading.Thread(target=run, args=[l_stocks, ])
            t.start()
            CollectorStatus.objects.create(ident=t.ident, status=1)
            msg = '采集器启动成功'
        elif len(json.loads(cs)) != 0 and action == 'stop':
            do = False
            t_ident = json.loads(cs)[0]['fields']['ident']
            t_list = threading.enumerate()
            for t in t_list:
                if t.ident == int(t_ident):
                    stop_thread(t)
                    CollectorStatus.objects.all().delete()
                    msg = '采集器终止'
                    do = True
                    break
            if not do:
                msg = '未找到采集器'
        else:
            msg = '未找匹配到动作:%s_%s' % (action, cs)
        status = 200
    except Exception as e:
        status = 500
        msg = '采集器%s失败' % action
        print(e)
    print(msg)
    sleep(1)
    return render(request, 'index.html', {'status': status, 'msg': msg})  # JsonResponse({'status': status, 'msg': msg})


def lb_hsl_sync(request):
    action = request.GET.get('action')
    cs = q_collectorstatus()
    nowday = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        l_stocks = list()
        lr_stocks = db_do_sql(
            sql_script='''SELECT t2.code FROM ( SELECT b.CODE, (b.nprice - IF(b.startprice>b.yprice,b.yprice,
            b.startprice))/IF(b.startprice>b.yprice,b.yprice,b.startprice)>=0.03 AS l, 
            (b.nprice - IF(b.startprice>b.yprice, b.yprice,b.startprice))/IF(b.startprice>b.yprice,
            b.yprice,b.startprice)<=0.05 AS u, b.time  FROM (SELECT *  FROM (select ROW_NUMBER() over( partition by 
            code order by time desc) r, t.* from stock.stockprice t WHERE t.date = '%s') a WHERE a.r = 1) b ) t2 
            WHERE t2.l=1 AND t2.u=1''' % nowday)
        print(l_stocks)
        for s in lr_stocks:
            st = s[0]
            l_stocks.append(st)
        t = threading.Thread(target=lb_hsl_run, args=[l_stocks, ])
        t.start()
        msg = '采集器启动成功'
        status = 200
    except Exception as e:
        status = 500
        msg = '采集器%s失败' % action
        print(e)
    print(msg)
    return render(request, 'index.html', {'status': status, 'msg': msg})


def lb_hsl_result(request):
    # 涨幅大于3%，小于5%
    # 换手率，大于5%，小于10%
    day = request.GET.get('day')
    if day:
        nowday = day
    else:
        nowday = datetime.datetime.now().strftime('%Y-%m-%d')
    # result = LbHsl2.objects.values('code').filter(date=nowday, turnoverrate__range=[5, 10]) \
    #     .annotate(t=Max('time'), d=Max('date'), r=Max('turnoverrate')).values('code', 't', 'd', 'r')
    result = db_do_sql(
        sql_script='''SELECT * FROM (SELECT ROW_NUMBER() over(PARTITION by t.code ORDER BY t.time DESC) r, t.* 
        FROM stock.lbhsl2 t WHERE t.date = '%s') a WHERE a.r = 1 and a.turnoverrate>=5 and a.turnoverrate<=10''' % nowday)
    l_stocks = list()
    print(result)
    stock_list = list(result)
    result_hsl_ltp = list()
    for s in stock_list:
        # st = s['code'] + '-' + str(s['r'])
        st = s[1] + '-' + str(s[4])
        l_stocks.append(st)
        # 流通盘 大于50亿，小于100亿
        if s[6] and s[6] >= 5000000000 and s[6] <= 20000000000:
            result_hsl_ltp.append(str(s[1]) + '-' + str(s[4]))
    return JsonResponse({'time': nowday, 'result_hsl_ltp_50_200': result_hsl_ltp, 'result_hsl_5_10': l_stocks})


def query_stock_sync_status(request):
    q_sIII = CollectorStatus.objects.all().values()
    return JsonResponse({'result': list(q_sIII)})
