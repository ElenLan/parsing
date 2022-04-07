# Вариант 1
# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем
# должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц
# сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть
# одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas. Сохраните
# в json либо csv.

import requests
from bs4 import BeautifulSoup as bs
from fake_headers import Headers
from pprint import pprint
import time
import random
import json

# https://hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text=
# Python+developer&from=suggest_post&customDomain=1
base_url = 'https://hh.ru'
url = base_url + '/search/vacancy?text=&page='
params = {'text': str(input('введите желаемую доллжность: ')),
          'page': 0}
header = Headers(headers=True).generate()
pages = 40
n = 1
while params['page'] <= pages:
    response = requests.get(url, headers=header, params=params)
    # with open('response.html', 'w', encoding='utf-8') as f:
    #     f.write(response.text)
    # html_file = ''
    # with open('response.html', 'r', encoding='utf-8') as f:
    #     html = f.read()
    dom = bs(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
    vacancy_list = []
    for vacancy in vacancies:
        vacancy_data = {}
        vacancy_name = vacancy.find('a', {'class': 'bloko-link'}).getText()
        vacancy_salary = str(vacancy.find('span', {'class': 'bloko-header-section-3'})).removeprefix(
            '<span class="bloko'
            '-header-section-3" '
            'data-qa="vacancy'
            '-serp__vacancy'
            '-compensation">'). \
            removesuffix('</span>').replace('<!-- --', '').replace('>', '').replace('\u202f', '').split(' ')
        salary_list = []
        salary_data = {}
        if 'None' in vacancy_salary:
            s_min = None
            s_max = None
            currency = None
        elif 'до' in vacancy_salary:
            s_min = None
            s_max = vacancy_salary[1]
            currency = vacancy_salary[-1]
        elif 'от' in vacancy_salary:
            s_min = vacancy_salary[1]
            s_max = None
            currency = vacancy_salary[-1]
        elif '-' in vacancy_salary:
            s_min = vacancy_salary[0]
            s_max = vacancy_salary[2]
            currency = vacancy_salary[-1]
        salary_data['min'] = s_min
        salary_data['max'] = s_max
        salary_data['currency'] = currency
        salary_list.append(salary_data)
        vacancy_link = vacancy.find('a', {'class': 'bloko-link'})['href']
        vacancy_data['name'] = vacancy_name
        vacancy_data['salary'] = salary_list
        vacancy_data['link'] = vacancy_link
        vacancy_list.append(vacancy_data)
        time.sleep(random.randint(1, 10))
        with open('vacancies.json', 'w', encoding='UTF-8') as f:
            json.dump(vacancy_list, f)
    button = int(dom.find_all('a', {'class': 'bloko-button'})[-2].text)
    pages = (button if pages < button else pages)
    params['page'] += 1

    pprint(vacancy_list)
    pprint(len(vacancy_list))

# python developer
