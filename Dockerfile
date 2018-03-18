FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

RUN ./manage.py collectstatic --noinput

RUN useradd test
RUN chown -R test /code
USER test
