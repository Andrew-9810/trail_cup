from django.db import models


class Person(models.Model):
    """Участники."""
    MAN = 'M'
    WOMAN = 'D'
    GENDER_CHOICES = [(MAN, 'M'), (WOMAN, 'Ж')]

    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MAN)
    birthday = models.DateField()
    keys = models.CharField(
        max_length=60, default=f'{surname}{name}{birthday}', blank=True
    )


class Group(models.Model):
    """Группы участников."""
    title = models.CharField(max_length=20)
    year_max = models.DateField()
    year_min = models.DateField()

class Season(models.Model):
    """Сезон забегов."""
    title = models.IntegerField()

class Scores(models.Model):
    """Очки за результат."""
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    result_place = models.IntegerField()
    scores = models.IntegerField()


class Run(models.Model):
    """Трейл забеги."""
    DAY = 'D'
    NIGHT = 'N'
    TYPE_CHOICES = [(DAY, 'M'), (NIGHT, 'Ж')]
    title = models.CharField(max_length=40)
    type_run = models.CharField(
        max_length=1, choices=TYPE_CHOICES, default=DAY
    )
    data_run = models.DateField()

class Result(models.Model):
    """Результаты трейла."""
    run = models.ForeignKey(Run, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    result_place = models.IntegerField()
    result_time = models.DateTimeField()
    # group =