from django.db import models


class Season(models.Model):
    """Сезон забегов."""
    title = models.IntegerField(verbose_name='Год')


    class Meta:
        verbose_name = 'сезон'
        verbose_name_plural = 'Сезоны'

    def __str__(self):
        return f'{self.title}'


class Person(models.Model):
    """Участники."""
    MAN = 'M'
    WOMAN = 'D'
    GENDER_CHOICES = [(MAN, 'M'), (WOMAN, 'Ж')]

    surname = models.CharField(verbose_name='Фамилия', max_length=30)
    name = models.CharField(verbose_name='Имя', max_length=30)
    gender = models.CharField(
        verbose_name='Пол', max_length=1, choices=GENDER_CHOICES, default=MAN
    )
    birthday = models.DateField(verbose_name='День рождения')


    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return f'{self.surname} {self.name} {self.birthday} | {self.pk} '


class TitleGroup(models.Model):
    """Заголовки групп."""
    title = models.CharField(verbose_name='Название', max_length=20)
    name_file_html = models.CharField(
        verbose_name='Имя для файла html', max_length=20,
        help_text=(
            'Используется в /media/data_html;'
            ' Имя должно быть латиницей без пробелов'
        )
    )


    class Meta:
        verbose_name = 'заголовок'
        verbose_name_plural = 'Заголовки групп'

    def __str__(self):
        return f'{self.title}'

class Group(models.Model):
    """Группы участников."""
    MAN = 'M'
    WOMAN = 'D'
    GENDER_CHOICES = [(MAN, 'M'), (WOMAN, 'Ж')]
    season = models.ForeignKey(
        Season, verbose_name='Сезон', on_delete=models.PROTECT, default=1900
    )
    title = models.ForeignKey(
        TitleGroup, verbose_name='Заголовок', on_delete=models.PROTECT
    )
    year_min = models.DateField(
        verbose_name='Год рождения от',
        help_text='Младшая граница возраста (в 2025 г для групп 14-17 лет 2011)'
    )
    year_max = models.DateField(
        verbose_name='Год рождения до',
        help_text='Старшая граница возраста (в 2025 г для групп 14-17 лет 2008)'
    )
    gender = models.CharField(
        verbose_name='Пол', max_length=1, choices=GENDER_CHOICES, default=MAN
    )


    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'Группы участников'

    def __str__(self):
        return f'{self.season} {self.title}'


class Scores(models.Model):
    """Очки за результат."""
    season = models.ForeignKey(
        Season, verbose_name='Сезон', on_delete=models.PROTECT, default=1900
    )
    result_place = models.IntegerField(verbose_name='Занятое место')
    scores = models.FloatField(verbose_name='Очки')


    class Meta:
        verbose_name = 'очки'
        verbose_name_plural = 'Очки'

    def __str__(self):
        return f'{self.season} {self.result_place} {self.scores}'


class Run(models.Model):
    """Трейл забеги."""
    DAY = 'D'
    NIGHT = 'N'
    TYPE_CHOICES = [(DAY, 'День'), (NIGHT, 'Ночь')]
    season = models.ForeignKey(
        Season, verbose_name='Сезон', on_delete=models.PROTECT, default=1900
    )
    title = models.CharField(verbose_name='Заголовок', max_length=40)
    type_run = models.CharField(
        verbose_name='Тип', max_length=4, choices=TYPE_CHOICES, default=DAY
    )
    data_run = models.DateField(verbose_name='Дата')
    is_published = models.BooleanField(
        verbose_name='Опубликовано', default=False
    )


    class Meta:
        verbose_name = 'забег'
        verbose_name_plural = 'Забеги'

    def __str__(self):
        return f'{self.data_run} {self.title}'


class Result(models.Model):
    """Результаты трейла."""
    run = models.ForeignKey(Run, verbose_name='Забег', on_delete=models.PROTECT)
    person = models.ForeignKey(
        Person, verbose_name='Участник', on_delete=models.PROTECT
    )
    result_place = models.IntegerField(verbose_name='Место')
    result_time = models.IntegerField(verbose_name='Время')
    distance = models.FloatField(verbose_name='Дистанция')
    group = models.ForeignKey(
        Group, verbose_name='Группа', on_delete=models.PROTECT, default=1
    )


    class Meta:
        verbose_name = 'результат'
        verbose_name_plural = 'Результаты'

    def __str__(self):
        return f'{self.run} {self.person}'

    def get_scores(self):
        """Получение очков по занятому месту."""
        season = self.group.season
        scores = Scores.objects.filter(
            season=season, result_place=self.result_place
        )
        if scores.exists():
            self.place_scores = scores[0].scores + self.distance
        else:
            self.place_scores = self.distance

    def get_type_run(self):
        """Получение типа гонки (день, ночь)."""
        self.type_run = self.run.type_run

