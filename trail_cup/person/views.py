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

def parce_csv(file):
    """Берет строчку файла и записывает ее в БД."""
    for i in file:
        fi = i[NAME].split()
        person = Person.objects.create(
            surname = fi[0],
            name = fi[1],
            gender = i[GENDER],
            birthday = f'{i[YEAR]}-01-01'
        )
        run = Run.objects.get(id=1)
        group = Group.objects.get(id=1)
        Result.objects.create(
            run = run,
            person = person,
            result_place = i[RES_PLACE],
            result_time = i[RES_TIME], #['“1:37:09” value has an invalid format. It must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format.']
            distance = i[DISTANCE],
            group = group

        )

def main_pr(request):
    path_csv = 'D:\\DEV\\trail_cup\\trail_cup\\person\\2025.csv'
    file_csv = read_csv(path_csv)
    parce_csv(file_csv)
    return None
