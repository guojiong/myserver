from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from stock.models import Stock


def index(request):
    return render(request, 'index.html')


def query_stock(request):
    searchCondition = {}
    code = request.POST.get('code')
    name = request.POST.get('name')
    origin = request.POST.get('origin')

    if code:
        searchCondition['code__contains'] = code
    if name:
        searchCondition['name__contains'] = name
    if origin:
        searchCondition['origin__contains'] = origin

    stocks = serializers.serialize('json', Stock.objects.filter(**searchCondition))
    return JsonResponse({'status': 200, 'result': stocks})


def update_or_create(request):

    code = request.POST.get('code')
    name = request.POST.get('name')
    origin = request.POST.get('origin')
    remark = request.POST.get('remark')

    Stock.objects.update_or_create(defaults={'code': code, 'name': name, 'origin': origin, 'remark': remark}, code=code)
    return JsonResponse({'status': 200})


def upload_file(request):
    file = request.files.get('file')
    # try:
    #     file = request.files['file']
    #     path = request.form['path']
    #     if path != '.':
    #         path = '/'.join(list(filter(not_empty, ('/'.join(list(filter(not_empty, path.split('\\'))))).split('/'))))
    #         if not os.path.exists(os.path.join(BASE_PATH, path)):
    #             abspath = BASE_PATH
    #             for p in path.split('/'):
    #                 abspath = os.path.join(abspath, p)
    #                 if not os.path.exists(abspath):
    #                     os.mkdir(abspath)
    #                 else:
    #                     continue
    #         else:
    #             abspath = os.path.join(BASE_PATH, path)
    #     else:
    #         abspath = BASE_PATH
    #     file.save(os.path.join(abspath, file.filename))
    #     os.system('start startup.vbs')
    #     return '200'
    # except Exception as e:
    #     print(e)
    #     return '500 %s' % e
