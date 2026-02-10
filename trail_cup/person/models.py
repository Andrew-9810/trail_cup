from django.db import models


class Season(models.Model):
    """Сезон забегов."""
    title = models.IntegerField()


class Person(models.Model):
    """Участники."""
    MAN = 'M'
    WOMAN = 'D'
    GENDER_CHOICES = [(MAN, 'M'), (WOMAN, 'Ж')]

    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MAN)
    birthday = models.DateField()


class TitleGroup(models.Model):
    """Заголовки групп."""
    title = models.CharField(max_length=20)


class Group(models.Model):
    """Группы участников."""
    MAN = 'M'
    WOMAN = 'D'
    GENDER_CHOICES = [(MAN, 'M'), (WOMAN, 'Ж')]
    season = models.ForeignKey(Season, on_delete=models.PROTECT, default=1900)
    title = models.ForeignKey(TitleGroup, on_delete=models.PROTECT)
    year_max = models.DateField()
    year_min = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MAN)

class Scores(models.Model):
    """Очки за результат."""
    season = models.ForeignKey(Season, on_delete=models.PROTECT, default=1900)
    result_place = models.IntegerField()
    scores = models.IntegerField()


class Run(models.Model):
    """Трейл забеги."""
    DAY = 'D'
    NIGHT = 'N'
    TYPE_CHOICES = [(DAY, 'День'), (NIGHT, 'Ночь')]
    season = models.ForeignKey(Season, on_delete=models.PROTECT, default=1900)
    title = models.CharField(max_length=40)
    type_run = models.CharField(
        max_length=4, choices=TYPE_CHOICES, default=DAY
    )
    data_run = models.DateField()
    is_published = models.BooleanField(
        verbose_name='Опубликовано', default=False
    )



class Result(models.Model):
    """Результаты трейла."""
    run = models.ForeignKey(Run, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    result_place = models.IntegerField()
    result_time = models.IntegerField(verbose_name='Время забега')
    distance = models.FloatField()
    group = models.ForeignKey(Group, on_delete=models.PROTECT, default=1)
