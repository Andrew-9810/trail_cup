from Tools.scripts.generate_token import update_file
from django import forms

from .models import Run


class LoadCsvForm(forms.Form):
    run_obj = Run.objects.values()
    choices = []
    for i in run_obj:
        value =(i['id'], i['title'],)
        choices.append(value)

    run = forms.ChoiceField(choices=choices)
    file = forms.FileField()