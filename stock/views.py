import json
from time import sleep
from django.http import JsonResponse
from django.shortcuts import render
import threading
from stock.dao.query import query
from stock.models import Stock, CollectorStatus
from stock.stock_sync import run, stop_thread


def index(request):
    return render(request, 'index.html')


def query_stock(request):
    code = request.POST.get('code')
    name = request.POST.get('name')
    origin = request.POST.get('origin')
    remark = request.POST.get('remark')

    result = query(code, name, origin, remark)
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
    stock_list = json.loads(query())[0]['fields']
    l_stocks = json.loads(query())["fields"]
    print(l_stocks)
    i = 0
    cs = CollectorStatus.objects.all()
    try:
        if len(cs) == 0 and action == 'start':
            t = threading.Thread(target=run)
            t.start()
            CollectorStatus.objects.create({'ident': t.ident, 'status': 1})
            msg = '采集器启动成功'
        elif len(cs) != 0 and action == 'stop':
            do = False
            t_ident = cs[0][1]
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
            msg = '未找匹配到动作:%s' % action
        status = 200
    except Exception as e:
        status = 500
        msg = '采集器%s失败' % action
        print(e)
    print(msg)
    while True:
        if i == 5:
            break
        i = i + 1
        sleep(1)
    return JsonResponse({'status': status, 'msg': msg})
