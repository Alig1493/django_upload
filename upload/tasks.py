from django_file_upload.celery import app
from upload.sq_projected_cap_scraper import process_file


@app.task
def run_file_upload_tasks(file_name):
    print("File tasks in progress.")
    process_file(input_file_path=file_name)
    print("File tasks processing completed.")
