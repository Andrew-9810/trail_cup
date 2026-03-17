import csv

from person.models import Result, Person, Group, Run

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


def parce_csv(path_csv, run_id):
    """Берет строчку файла и записывает ее в БД."""
    try:
        file_csv = read_csv(path_csv)
        run = Run.objects.get(id=run_id)
        for line in file_csv:
            fi = line[NAME].split()
            person, _ = Person.objects.get_or_create(
                surname = fi[0],
                name = fi[1],
                gender = line[GENDER],
                birthday = f'{line[YEAR]}-01-01'
            )
            group_obj = defining_group(
                    gender=line[GENDER],
                    birthday=f'{line[YEAR]}-01-01',
                    season=run.season.id
            )
            if not group_obj:
                continue
            Result.objects.create(
                run = run,
                person = person,
                result_place = line[RES_PLACE],
                result_time = converter_time(line[RES_TIME]),
                distance = line[DISTANCE],
                group = group_obj
            )
        return True
    except Exception as err:
        return err

def counting_scores(scores: list, quantity_event: int) -> int:
    """Возвращает quantity_event лучших очков."""
    result = 0
    scores.sort(reverse=True)
    for i in scores[:quantity_event]:
        result += i
    return result
