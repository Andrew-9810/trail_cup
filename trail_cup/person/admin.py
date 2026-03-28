from django.contrib import admin

from .models import Season, Scores, Run, Result, Person, Group, TitleGroup

LIST_PER_PAGE = 15 # Элементов на листе при пагинации


class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'run',
        'person',
        'result_place',
        'result_time',
        'distance',
        'group',
    )
    list_filter = ('run', 'person',)
    list_per_page = LIST_PER_PAGE


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'season',
        'title',
        'year_min',
        'year_max',
        'gender',
    )
    list_filter = ('season',)
    list_per_page = LIST_PER_PAGE


class RunAdmin(admin.ModelAdmin):
    list_display = (
        'season',
        'title',
        'type_run',
        'data_run',
        'is_published',
    )
    list_editable = (
        'title',
        'type_run',
        'data_run',
        'is_published',
    )
    list_filter = ('is_published', 'type_run', 'season')
    list_per_page = LIST_PER_PAGE


class ScoresAdmin(admin.ModelAdmin):
    list_display = (
        'season',
        'result_place',
        'scores',
    )
    list_editable = (
        'result_place',
        'scores',
    )
    list_filter = ('season',)
    list_per_page = LIST_PER_PAGE


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'surname',
        'name',
        'gender',
        'birthday',
    )
    list_editable = (
        'surname',
        'name',
        'gender',
        'birthday',
    )
    list_per_page = LIST_PER_PAGE

admin.site.register(Result, ResultAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(Season)
admin.site.register(Scores, ScoresAdmin)
admin.site.register(TitleGroup)
admin.site.register(Person, PersonAdmin)

admin.site.empty_value_display = 'Не задано'