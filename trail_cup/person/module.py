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

def get_result(group:int, run:list):
    """Возвращает объект результата участников по группе."""
    # Предполагается, что все участники по группе в единственном экземпляре
    # События run должны иметь свойство опубликовано
    person_set = set()
    event_list = []
    result_list = []
    for event in run:
        result = Result.objects.filter(run=event, group=group)
        for pers in result:
            person_set.add(pers.person) # получаю pk по которому выведу ФИ
        result_list.append(result)
    return result_list

def defining_group(gender: str, birthday: str, season: int):
    """Определение группы по году рождения и полу."""
    group = Group.objects.filter(season=season, gender=gender,
        year_max__lte=birthday, year_min__gte = birthday
    )
    if len(group) == 1:
        return group[0]
    else:
        return False
