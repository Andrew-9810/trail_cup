from django.shortcuts import render
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.conf import settings
from jinja2 import Environment, FileSystemLoader

from .models import Result, Person, Run, Group
from .module import (
    NAME, YEAR, RES_TIME, RES_PLACE, DISTANCE, GENDER, read_csv, converter_time,
    get_result, defining_group
)
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
            path_file = f'{settings.MEDIA_ROOT}\\{form.cleaned_data["file"].name}'
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
    return render(request, template_name='index.html', context=context)


def parce_csv(path_csv, run_id):
    """Берет строчку файла и записывает ее в БД."""
    try:
        file_csv = read_csv(path_csv)
        run = Run.objects.get(id=run_id)
        for line in file_csv:
            fi = line[NAME].split()
            person, _ = Person.objects.get_or_create(
                surname = fi[0],
                name = fi[1],
                gender = line[GENDER],
                birthday = f'{line[YEAR]}-01-01'
            )
            group_obj = defining_group(
                    gender=line[GENDER],
                    birthday=f'{line[YEAR]}-01-01',
                    season=run.season.id
            )
            if not group_obj:
                continue
            Result.objects.create(
                run = run,
                person = person,
                result_place = line[RES_PLACE],
                result_time = converter_time(line[RES_TIME]),
                distance = line[DISTANCE],
                group = group_obj
            )
        return True
    except Exception as err:
        return err

def group(request):
    """Получение результата по группе"""
    gr = 1 # Запрос по 1 группе Тест
    races = [1, 2] # Это будут опубликованные события

    main_dict = {}
    result_person = {}
    sum_scores = {}
    sum_distance = {}
    for run in races:
        res = get_result(gr, run)
        for person_id in res.keys():
            if person_id in result_person:
                result_person[person_id].append(res[person_id][0])
                sum_scores[person_id] += res[person_id][0]['result_person'].scores
                sum_distance[person_id] += res[person_id][0]['result_person'].distance
            else:
                result_person[person_id] = res[person_id]
                sum_scores[person_id] = res[person_id][0]['result_person'].scores
                sum_distance[person_id] = res[person_id][0]['result_person'].distance
    if (result_person.keys() == sum_scores.keys()
            and result_person.keys() == sum_distance.keys()
    ):
        for person_id in result_person.keys():
            person = Person.objects.get(id=person_id)
            main_dict[person_id] = {
                'person_name': person.name,
                'person_surname': person.surname,
                'result_person': result_person[person_id],
                'count_res_pers': len(result_person[person_id]),
                'sum_scores': sum_scores[person_id],
                'sum_distance': sum_distance[person_id]
            }
    else:
        return render(
            request, template_name='good.html', context={
                'mess': 'error - не совпадают дист. очки и кол-во участников'
            }
        )
    context = {
        'main_dict': main_dict,
    }
    template_name = environment.get_template('result.html')
    results_filename = f'{path_templates}\\my_file.html'
    with open(results_filename, mode="w", encoding="utf-8") as results:
        results.write(template_name.render(context))

    return render(request, context={'mess': 'good'}, template_name='good.html')

