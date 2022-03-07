FROM python:3.8.12
MAINTAINER SAM
ENV PYTHONUNBUFFERED 1
COPY pip.conf /root/.pip/pip.conf
RUN mkdir -p /var/www/html/mysite
WORKDIR /var/www/html/mysite
ADD . /var/www/html/mysite

RUN \
  pip install -r requirements.txt && \
  python manage.py makemigrations && \
  python manage.py migrate && \
  uwsgi --ini /var/www/html/mysite/uwsgi.ini

