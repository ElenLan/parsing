# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет
# добавлять только новые вакансии/продукты в вашу базу.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты).

from pymongo import MongoClient
from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs
from fake_headers import Headers
from pprint import pprint
import json

# with open('vacancies.json', 'r', encoding='UTF-8') as f:
#     vacancy = json.load(f)

# for vacancy_db in vacancy:
#     vacancies.insert_one(vacancy_db)

base_url = 'https://hh.ru'
url = base_url + '/search/vacancy?text=&page='
params = {'text': str(input('введите желаемую доллжность: ')),
          'page': 0}
header = Headers(headers=True).generate()
pages = 40
n = 1
try:
    while params['page'] <= pages:
        client = MongoClient('127.0.0.1', 27017)

        db = client['hhru']
        vacancies_db = db.vacancies
        response = requests.get(url, headers=header, params=params)
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
                s_max = int(vacancy_salary[1])
                currency = vacancy_salary[-1]
            elif 'от' in vacancy_salary:
                s_min = int(vacancy_salary[1])
                s_max = None
                currency = vacancy_salary[-1]
            elif '–' in vacancy_salary:
                s_min = int(vacancy_salary[0])
                s_max = int(vacancy_salary[2])
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

        button = int(dom.find_all('a', {'class': 'bloko-button'})[-2].text)
        pages = (button if pages < button else pages)
        params['page'] += 1

        pprint(vacancy_list)

        try:                                             #добавление новых записей в базу
            for vacancy_db in vacancy_list:
                vacancies_db.insert_one(vacancy_db)
                if vacancies_db.find_one({'name': vacancy_db['name'],
                                          'link': vacancy_db['link']}):
                    print('запись уже есть')
                    # vacancies_db.delete_one(vacancy_db)
        except:
            print('опаньки')



except IndexError:
    print('end')

'''проверка на з/п. код по лекции, но результата не выдаёт. пыталась добраться через salary - тоже не вышло)
# sal_for_input = input('Введите желаемую з/п: ')
# for v in vacancies_db.find({'$or': [{'min': {'$gte': sal_for_input}}, {'max': {'$gte': sal_for_input}}]}):
#     print(v)

# for v in vacancies_db.find({'$or': [{'salary': {'min': {'$gte': sal_for_input}}}, {'salary': {'max': {'$gte': sal_for_input}}}]}):
#     print(v)
'''
# python developer
