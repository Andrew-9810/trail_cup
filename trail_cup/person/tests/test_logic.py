from tokenize import group

from django.test import TestCase
from person.models import Season, Run, Result, Person, Group, TitleGroup

class ModelTest(TestCase):
    """Тест моделей."""
    def test_count_season(self):
        """Тест количества создаваемых объектов"""
        season_title = 2025
        Season.objects.create(title=season_title)
        season = Season.objects.count()
        self.assertEqual(season, 1)

    def test_data_season(self):
        """Тест данных создаваемого объекта"""
        season_title = 2025
        Season.objects.create(title=season_title)
        season = Season.objects.all()
        self.assertEqual(season[0].title, season_title)

    def test_count_run(self):
        """Тест количества создаваемых объектов"""
        season_title = 2025
        season = Season.objects.create(title=season_title)
        Run.objects.create(
            season=season, title='Test_start', type_run='D',
            data_run='2026-01-23'
        )
        run = Run.objects.count()
        self.assertEqual(run, 1)

    def test_data_run(self):
        """Тест данных создаваемого объекта"""
        season_title = 2025
        season = Season.objects.create(title=season_title)
        title = 'Test_start'
        type_run = 'D'
        data_run = '2026-01-23'
        Run.objects.create(
            season=season, title=title, type_run=type_run,
            data_run=data_run
        )
        run = Run.objects.all()[0]
        result = f'{run.season.title}{run.title}{run.type_run}{run.data_run}'
        answer = f'{season_title}{title}{type_run}{data_run}'
        self.assertEqual(result, answer)

    def test_count_person(self):
        """Тест количества создаваемых объектов"""
        surname = 'surname'
        name = 'name'
        gender = 'M'
        birthday = '2026-01-23'
        Person.objects.create(
            surname=surname, name=name, gender=gender, birthday=birthday
        )
        person = Person.objects.count()
        self.assertEqual(person, 1)

    def test_data_person(self):
        """Тест данных создаваемого объекта"""
        surname = 'surname'
        name = 'name'
        gender = 'M'
        birthday = '2026-01-23'
        Person.objects.create(
            surname=surname, name=name, gender=gender, birthday=birthday
        )
        per = Person.objects.all()[0]
        result = f'{per.surname}{per.name}{per.gender}{per.birthday}'
        answer = f'{surname}{name}{gender}{birthday}'
        self.assertEqual(result, answer)

    def test_count_group(self):
        """Тест количества создаваемых объектов"""
        season_title = 2025
        title_group = 'Test_group'
        year_max = '2025-01-01'
        year_min = '2026-01-01'
        season = Season.objects.create(title=season_title)
        title = TitleGroup.objects.create(title=title_group)
        Group.objects.create(
            season=season, title=title, year_max=year_max, year_min=year_min
        )
        group = Group.objects.count()
        self.assertEqual(group, 1)

    def test_data_group(self):
        """Тест данных создаваемого объекта"""
        season_title = 2025
        title_group = 'Test_group'
        year_max = '2025-01-01'
        year_min = '2026-01-01'
        season = Season.objects.create(title=season_title)
        title = TitleGroup.objects.create(title=title_group)
        Group.objects.create(
            season=season, title=title, year_max=year_max, year_min=year_min
        )
        gr = Group.objects.all()[0]
        result = f'{gr.season.title}{gr.title.title}{gr.year_max}{gr.year_min}'
        answer = f'{season_title}{title_group}{year_max}{year_min}'
        self.assertEqual(result, answer)

    def test_count_result(self):
        """Тест количества создаваемых объектов"""
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
        Result.objects.create(
            run=run, person=person, result_place=result_place,
            result_time=result_time, distance=distance, group=group
        )
        res = Result.objects.count()
        self.assertEqual(res, 1)

    def test_data_result(self):
        """Тест данных создаваемого объекта"""
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
        result = (f'{res.run.title}{res.person.surname}{res.result_place}'
                  f'{res.result_time}{res.distance}{res.group.year_max}')
        answer = (f'{title}{surname}{result_place}{result_time}{distance}'
                  f'{year_max}')
        self.assertEqual(result, answer)





