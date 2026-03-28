from django.contrib import admin

from .models import Season, Scores, Run, Result, Person, Group, TitleGroup

admin.site.register(Run)
admin.site.register(Season)
admin.site.register(Scores)
admin.site.register(Result)
admin.site.register(Person)
admin.site.register(Group)
admin.site.register(TitleGroup)