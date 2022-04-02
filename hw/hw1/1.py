# 1. Посмотреть документацию к API GitHub, разобраться как вывести список наименований репозиториев для конкретного
# пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

url = 'https://api.github.com/users/ElenLan/repos'
response = requests.get(url)

with open('repos.json', 'w') as f:
    for i in response.json():
        repos = i['name']
        json.dump(repos, f)
        print(repos)
