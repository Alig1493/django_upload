FROM python:3.6.0-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1

ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt --no-cache-dir

RUN chmod -R 777 ../media/

RUN useradd django_upload
RUN chown -R django_upload /app
USER django_upload
COPY . /app
RUN ./manage.py collectstatic --no-input