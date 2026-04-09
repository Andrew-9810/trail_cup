# trail_cup
Результаты кубка трейлов

Создать виртуальное окружение в директории trail_cup, рядом с Readme, requirment
Linux:
python3 -m venv venv
Windows:
python -m venv venv
Создть .env рядом с Readme, requirment

Выполнить:
Linux:
source venv/bib/activate
Windows:
source venv/Script/activate

Linux:
python3 -r requirement.txt
Windows:
python -r requirement.txt

В директории trail_cup/trail_cup
Применить миграции:
python3 manage.py makemigrations
python3 manage.py migrate

Собрать статику
python3 manage.py collectstatic

Создать суперпользователя
python3 manage.py createsuperuser