from django.shortcuts import render
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.conf import settings

from .models import Season, Group
from .module import parce_csv, create_file_html
from .forms import LoadCsvForm
from .tasks import create_file_html


def load_csv(request):
    """Получить путь к файлу, получить объект мероприятия."""
    if request.method == 'POST':
        file_data = {
            'file': SimpleUploadedFile(
                request.FILES['file'].name, request.FILES['file'].read()
            )
        }
        form = LoadCsvForm(request.POST, file_data)
        if form.is_valid():
            path_file = f'{settings.MEDIA_ROOT}\\{form.cleaned_data["file"].name}\\load_csv'
            run_id = form.cleaned_data['run']
            with open(path_file, 'w', newline='') as f:
                myfile = File(f)
                myfile.write(form.cleaned_data['file'].read().decode('cp1251'))
            switch = parce_csv(path_file, run_id)
            if switch:
                print('load')
            else:
                print(switch)
    else:
        form = LoadCsvForm()
    context = {
        'form': form
    }
    return render(request, template_name='load_csv.html', context=context)

def group(request, group_id: int):
    """Получение результата по группе"""
    create_file_html.delay(group_id)
    return render(request, context={'mess': 'good'}, template_name='good.html')

def index(request):
    """Главная страница, выбор сезона"""
    seasons = Season.objects.all()
    return render(
        request, context={'seasons': seasons}, template_name='index.html'
    )

def choice(request, season:int):
    """Выбор группы по сезону."""
    groups = Group.objects.filter(season_id=season)
    return render(
        request, context={'groups': groups}, template_name='choice_group.html'
    )

