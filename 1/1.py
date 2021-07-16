# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import os

username = 'ElenLan'
token = os.environ.get("GITHUB_TOKEN")
r = requests.get('https://api.github.com', auth=(username, token))
repos = requests.get('https://api/github.com/users', auth=(username, token))
