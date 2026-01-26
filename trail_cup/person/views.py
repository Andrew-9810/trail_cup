from .models import Result, Person, Run, Group

from django.shortcuts import render

from .module import (
    NAME, YEAR, RES_TIME, RES_PLACE, DISTANCE, GENDER, read_csv, converter_time
)


def parce_csv(request):
    """Берет строчку файла и записывает ее в БД."""
    path_csv = 'D:\\DEV\\trail_cup\\trail_cup\\person\\2025.csv'
    file_csv = read_csv(path_csv)
    for line in file_csv:
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
    return None

