import csv

from django.shortcuts import render

NAME = 0
YEAR = 1
RES_TIME = 2
RES_PLACE = 3
DISTANCE = 4

def read_csv(path):
    """Получает путь к файлу csv отдает считанный в переменную файл."""
    persons = []
    with open(path, newline='', encoding='cp1251') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            data = [
                row[NAME], row[YEAR], row[RES_TIME],
                row[RES_PLACE], row[DISTANCE]
            ]
            persons.append(data)
    return persons

def parce_csv(file):
    """Берет строчку файла и записывает ее в БД."""
    for i in file:
        print(i)

def main_pr():
    path_csv = '2025.csv'
    file_csv = read_csv(path_csv)
    parce_csv(file_csv)

main_pr()