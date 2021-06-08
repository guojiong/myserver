import requests

url = 'http://127.0.0.1:8000/ucstock/'
data = {'code': 600001, 'name': '测试1', 'origin': 'sh', 'remark': ''}
requests.post(url, data)
