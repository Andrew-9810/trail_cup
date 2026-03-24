from trail_cup.celery import app
from .module import create_file_html

@app.task
def create_file_html(group_id: int):
    create_file_html(group_id)