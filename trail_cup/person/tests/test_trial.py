from django.test import TestCase
from person.module import converter_time, add_simbol_zero, get_result
from person.models import Season, Run, Result, Person, Group, TitleGroup


class FuncTest(TestCase):
    """Тест функций."""

    def test_converter_time(self):
        """Тест функции converter_time"""
        hour = 60*60
        minute = 60
        data = (
            ('11:37:19', 11 * hour + 37 * minute + 19),
            ('01:07:09', 1 * hour + 7 * minute + 9),
            (11 * hour + 37 * minute + 19, '11:37:19'),
            (1 * hour + 7 * minute + 9, '01:07:09'),
            (0 * hour + 37 * minute + 0, '00:37:00'),
        )
        for i in data:
            result = converter_time(i[0])
            answer = i[1]
            self.assertEqual(result, answer)

    def test_add_simbol_zero(self):
        """Тестирование функции добавления нуля."""
        data = (
            (0, '00'), (33, '33')
        )
        for i in data:
            result = add_simbol_zero(i[0])
            answer = i[1]
            self.assertEqual(result, answer)

    def test_get_result(self):
        """Тестирование функции получения результата по группе."""
        season_title = 2025
        season = Season.objects.create(title=season_title)
        title = 'Test_start'
        type_run = 'D'
        data_run = '2026-01-23'
        surname = 'surname'
        name = 'name'
        gender = 'M'
        birthday = '2026-01-23'
        result_place = 1
        minute = 47
        second = 56
        result_time = 60 * minute + second
        distance = 3.5
        title_g = 'Test_group'
        title_group = TitleGroup.objects.create(title=title_g)
        year_max = '2025-01-01'
        year_min = '2026-01-01'
        run = Run.objects.create(
            season=season, title=title, type_run=type_run,
            data_run=data_run
        )
        person = Person.objects.create(
            surname=surname, name=name, gender=gender, birthday=birthday
        )
        group = Group.objects.create(
            season=season, title=title_group, year_max=year_max,
            year_min=year_min
        )
        res = Result.objects.create(
            run=run, person=person, result_place=result_place,
            result_time=result_time, distance=distance, group=group
        )
        x = get_result(group=1, run=[1])
        print(x)
        result = (f'{res.run.title}{res.person.surname}{res.result_place}'
                  f'{res.result_time}{res.distance}{res.group.year_max}')
        answer = (f'{title}{surname}{result_place}{result_time}{distance}'
                  f'{year_max}')
        self.assertEqual(result, answer)