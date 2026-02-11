import csv

from person.models import Result, Person, Group

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

def get_result(group:int, run:int):
    """Возвращает объект результата участников по группе."""
    # Предполагается, что все участники по группе в единственном экземпляре
    # События run должны иметь свойство опубликовано
    person_result = {}
    result = Result.objects.filter(group=group, run=run)
    for res in result:
        res_time = converter_time(res.result_time)
        res.result_time = res_time
        res.get_scores()
        person_result[res.person_id] = [{'result_person': res}]
    return person_result

def defining_group(gender: str, birthday: str, season: int):
    """Определение группы по году рождения и полу."""
    group = Group.objects.filter(season=season, gender=gender,
        year_max__lte=birthday, year_min__gte = birthday
    )
    if len(group) == 1:
        return group[0]
    else:
        return False

def sort_result(value: dict, reverce: bool = False) -> dict:
    """Сортировка"""
    result = dict(sorted(
        value.items(),
        key=lambda item: (
            item[1]['sum_scores'],
            item[1]['sum_distance'],
            item[1]['count_res_pers']
        ),
        reverse=reverce
    ))
    return result
