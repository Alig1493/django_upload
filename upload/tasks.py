from __future__ import absolute_import, unicode_literals
from django_file_upload.celery import app

from upload.models import File
from upload.sq_projected_cap_scraper import process_file


@app.task
def add(x, y):
    return x + y


@app.task
def process(id):
    instance = File.objects.get(id=id)
    process_file(input_file_path=instance.file_field.path)
