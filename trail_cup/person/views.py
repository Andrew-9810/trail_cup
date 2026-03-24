from django.shortcuts import render
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.conf import settings
from jinja2 import Environment, FileSystemLoader

from .models import Result, Person, Run, Season, Group
from .module import get_result, sort_result, parce_csv, counting_scores
from .forms import LoadCsvForm


path_templates = f'{settings.BASE_DIR}\\person\\templates\\'
environment = Environment(loader=FileSystemLoader(
    path_templates
))


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
    races = Run.objects.filter(is_published=True).order_by('data_run')
    main_dict = {}
    result_person = {}
    sum_scores = {}
    sum_distance = {}
    sum_race = {}
    for index, run in enumerate(races): # Текущий забег
        res = get_result(group_id, run.id)
        for person_id in res.keys(): # Добавление участников
            if person_id in result_person:
                result_person[person_id].append(res[person_id][0])
                calculated_scores = (
                    res[person_id][0]['result_person'].place_scores
                )
                sum_scores[person_id].append(calculated_scores)
                sum_distance[person_id] += res[person_id][0]['result_person'].distance
                sum_race[person_id] += 1
            else:
                if index != 0: # Участник включается в кубок не с первого события
                    result_person[person_id] = [
                        {'result_person': Result.objects.none()} for _ in range(index)
                    ]
                    result_person[person_id].append(res[person_id][0])
                else:
                    result_person[person_id] = res[person_id]
                calculated_scores = (
                    res[person_id][0]['result_person'].place_scores
                )
                sum_scores[person_id] = [calculated_scores]
                sum_distance[person_id] = res[person_id][0][
                    'result_person'].distance
                sum_race[person_id] = 1
        if index != 0: # проверка отсутствия участника на забеге
            person_pass = set(result_person.keys()) - set(res.keys())
            for person_id in person_pass:
                result_person[person_id].append(
                    {'result_person': Result.objects.none()}
                )
    if result_person.keys() == sum_scores.keys() == sum_distance.keys():
        for person_id in result_person.keys():
            person = Person.objects.get(id=person_id)
            main_dict[person_id] = {
                'person_name': person.name,
                'person_surname': person.surname,
                'result_person': result_person[person_id],
                'count_res_pers': sum_race[person_id],
                'sum_scores': counting_scores(sum_scores[person_id], settings.SCORING_STAGES),
                'sum_distance': sum_distance[person_id]
            }
    else:
        return render(
            request, template_name='good.html', context={
                'mess': 'error - не совпадают дист. очки и кол-во участников'
            }
        )
    main_dict = sort_result(main_dict, reverce=True)
    context = {
        'main_dict': main_dict, 'races': races
    }
    template_name = environment.get_template('result.html')
    group_name = Group.objects.get(id=group_id).title.name_file_html

    results_filename = f'{settings.MEDIA_ROOT}\\data_html\\{group_name}.html'
    with open(results_filename, mode="w", encoding="utf-8") as results:
        results.write(template_name.render(context))

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

