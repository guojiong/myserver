import datetime
import json
from time import sleep

import requests
from django.core import serializers
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
        lr_stocks = db_do_sql(  # AND time>='14:25' AND t.time <='14:40' ORDER BY t.time DESC
            sql_script='''SELECT DISTINCT * FROM (SELECT t.code, (t.nprice-t.startprice)/t.startprice AS ns, 
            (t.nprice-t.yprice)/t.yprice AS ny, t.time FROM stock.stockprice t WHERE date = '%s' 
            
            ) a WHERE a.ns >= 0.03 AND a.ns <= 0.05 
            AND a.ny >= 0.03 AND a.ny <= 0.05''' % nowday)
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
    nowday = datetime.datetime.now().strftime('%Y-%m-%d')
    result = LbHsl2.objects.filter(date=nowday, turnoverrate__range=[5, 10]).values('code',
                                                                                   'turnoverrate').distinct()
    l_stocks = list()
    stock_list = list(result)
    for s in stock_list:
        st = s['code'] + '-' + str(s['turnoverrate'])
        l_stocks.append(st)
    # 流通盘 大于50亿，小于100亿
    result_hsl_ltp = list()
    for l in l_stocks:
        ll = l.split('-')
        url = 'http://qt.gtimg.cn/q=%s' % ll[0]
        result = requests.get(url)
        r_json = result.text[12:-3].split('~')
        try:
            if int(r_json[-2]) > 5000000000:
                result_hsl_ltp.append(ll[0] + '-' + r_json[-2])
        except:
            continue
    return JsonResponse({'time': nowday, 'result_hsl_ltp_50_200': result_hsl_ltp, 'result_hsl_5_10': l_stocks})


def query_stock_sync_status(request):
    q_sIII = CollectorStatus.objects.all().values()
    return JsonResponse({'result': list(q_sIII)})
