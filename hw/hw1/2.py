# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое, требующее
# авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

# Список объектов Национального парка, вход по apikey
import requests
import json
url = 'https://developer.nps.gov/api/v1/places'
api_key = '***'
parkCode = 'acad'
params = {'parkCode': parkCode, 'api_key': api_key}
response = requests.get(url, params=params)
j_data = response.json()
with open('obj.json', 'w') as f:
    for i in j_data['data']:
        names = i['title']
        print(names)
        json.dump(names, f)

