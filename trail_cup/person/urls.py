from django.urls import path

from .views import index, group, load_csv,  choice

urlpatterns = [
    # Если вызван URL без относительного адреса (шаблон — пустые кавычки),
    # то вызывается view-функция index() из файла views.py
    path('', index),
    path('choice/<int:season>/', choice, name='choice'),
    path('group_result/<int:group_id>/', group, name='group_result'),
    path('load_csv/', load_csv),
]