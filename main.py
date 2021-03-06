from datetime import timedelta, datetime
import csv

from tempoapiclient import client


# Данная функция генерирует дни в промежутке недели
def date_range(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + timedelta(n)


# Создается словарь с днями недели и значением по умолчаению
def gen_date_dict(start_dt, end_dt):
    result = {}
    start_dt = datetime.strptime(start_dt, "%Y-%m-%d")
    end_dt = datetime.strptime(end_dt, "%Y-%m-%d")
    for dt in date_range(start_dt, end_dt):
        result[dt.strftime("%Y-%m-%d")] = 'данные отсутствуют'
    return result

# Даты для которых берем данные
date_from = "2021-01-11"
date_to = "2021-01-17"
# Подключение по API и получение данных
tempo = client.Tempo(
    auth_token="67Zv2sVtRB9zv6Rz0jeWxFjO0ewZI9",
    base_url="https://api.tempo.io/core/3")
#
worklogs = tempo.get_worklogs(
   dateFrom=date_from,
   dateTo=date_to
  )

# Словарь с загатовленными датами в течении недели и результрующий словарь
dates = gen_date_dict(date_from, date_to)
work_data = {}
# цикл получения данных и добавления их в словарь, обработка результатов и сложение времени
for worklog in worklogs:
    name = worklog['author']['displayName']
    date = worklog['startDate']
    spent_time_s = worklog['timeSpentSeconds']

    if work_data.get(name, False):
        if isinstance(work_data[name][date], int):
            work_data[name][date] += spent_time_s
        else:
            work_data[name][date] = spent_time_s
    else:
        work_data[name] = dates.copy()
        work_data[name][date] = spent_time_s



names_list = []

with open('export-users.csv', newline='') as csvfile:
    names = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
    names.pop(0)
    for row in names:
        names_list.append(row[1])

for name in names_list:
    if work_data.get(name, False):
        pass
    else:
        work_data[name] = dates.copy()

# Цикл для вывода результатов и перевода секунд в часы
for user, dates in work_data.items():
    for date, time in dates.items():
        if isinstance(time, int):
            print(user, date, str(timedelta(seconds=time)))
        else:
            print(user, date, time)
