import csv

from .models import Result, Person, Run, Group


from django.shortcuts import render

NAME = 0
YEAR = 1
RES_TIME = 2
RES_PLACE = 3
DISTANCE = 4
GENDER = 5

def read_csv(path):
    """Получает путь к файлу csv отдает считанный в переменную файл."""
    persons = []
    with open(path, newline='', encoding='cp1251') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            data = [
                row[NAME], row[YEAR], row[RES_TIME],
                row[RES_PLACE], row[DISTANCE], row[GENDER]
            ]
            persons.append(data)
    return persons


def add_simbol_zero(arg):
    """Добавляет ноль в начало строки если в строке один символ."""
    data = str(arg)
    if len(data) < 2:
        return data.zfill(2)
    elif len(data) == 2:
        return data
    else:
        raise ValueError("Получил число больше 2х символов")


def converter_time(arg):
    """Преобразовывает время в число секунд, и наоборот."""
    hour_sec = 60 * 60
    minute_sec = 60
    if isinstance(arg, str):
        hour, minute, second = arg.split(':')
        result = int(hour) * hour_sec + int(minute) * minute_sec + int(second)
    elif isinstance(arg, int):
        hour = arg // hour_sec
        remaining_minutes = arg - hour * hour_sec
        minute = remaining_minutes // minute_sec
        remaining_seconds = remaining_minutes - minute * minute_sec
        res = list()
        for i in [hour, minute, remaining_seconds]:
            res.append(add_simbol_zero(i))
        result = f'{res[0]}:{res[1]}:{res[2]}'
    else:
        raise ValueError("Должен получить либо строку либо число!")
    return result




def parce_csv(file):
    """Берет строчку файла и записывает ее в БД."""
    for line in file:
        fi = line[NAME].split()
        person = Person.objects.create(
            surname = fi[0],
            name = fi[1],
            gender = line[GENDER],
            birthday = f'{line[YEAR]}-01-01'
        )
        run = Run.objects.get(id=1)
        group = Group.objects.get(id=1)
        Result.objects.create(
            run = run,
            person = person,
            result_place = line[RES_PLACE],
            result_time = converter_time(line[RES_TIME]),
            distance = line[DISTANCE],
            group = group

        )

def main_pr(request):
    path_csv = 'D:\\DEV\\trail_cup\\trail_cup\\person\\2025.csv'
    file_csv = read_csv(path_csv)
    parce_csv(file_csv)
    return None
