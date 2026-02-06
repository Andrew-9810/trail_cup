from django.urls import path

from .views import parce_csv, group, load_csv

urlpatterns = [
    # Если вызван URL без относительного адреса (шаблон — пустые кавычки),
    # то вызывается view-функция index() из файла views.py
    path('parce_csv/', parce_csv),
    path('group/', group),
    path('load_csv/', load_csv),
]