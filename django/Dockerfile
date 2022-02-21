FROM python:3.9-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y --no-install-recommends \
unixodbc-dev \
unixodbc \
libpq-dev 

COPY /requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

RUN mkdir /backend
COPY ./backend /backend
WORKDIR /backend
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

CMD python manage.py makemigrations && \
python manage.py collectstatic --no-input && \
python manage.py migrate && \
gunicorn backend.wsgi:application --bind 0.0.0.0:8000