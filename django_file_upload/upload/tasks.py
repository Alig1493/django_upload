from django_file_upload.celery import app


# A task being bound means the first argument to the task will always be the task instance (self),
# just like Python bound methods:
from .sq_projected_cap_scraper import process_file


@app.task(bind=True)
def run_file_upload_tasks(self, file_name, file_date):
    print("File tasks in progress.")
    process_file(input_file_path=file_name, input_file_date=file_date)
    print("File tasks processing completed.")
