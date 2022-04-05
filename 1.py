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

# https://hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text=
# Python+developer&from=suggest_post&customDomain=1

base_url = 'https://hh.ru'
url = base_url + '/search/vacancy?text=python+developer&clusters=true&ored_clusters=true&enable_snippets=true'
header = Headers(headers=True).generate()
response = requests.get(url, headers=header)
# with open ('response.html', 'w', encoding='utf-8') as f:
#     f.write(response.text)
dom = bs(response.text, 'html.parser')
vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
# vacancy_salary = dom.find('span', {'class': 'bloko-header-section-3'}).text
# pprint(vacancy_salary) -- Здесь возвращает результат методом find  одном экземпляре
vacancy_list = []
for vacancy in vacancies:
    vacancy_data = {}
    vacancy_name = vacancy.find('a', {'class': 'bloko-link'}).getText()
    vacancy_salary = vacancy.find('span', {'class': 'bloko-header-section-3'}).getText() # метод text и getText возвращают ошибку
    # pprint(vacancy_salary)
    vacancy_link = vacancy.find('a', {'class': 'bloko-link'})['href']
    vacancy_data['name'] = vacancy_name
    vacancy_data['salary'] = vacancy_salary
    vacancy_data['link'] = vacancy_link
    vacancy_list.append(vacancy_data)
pprint(vacancy_list)
