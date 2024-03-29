FROM python:3.8.12
MAINTAINER SAM
ENV PYTHONUNBUFFERED 1
COPY pip.conf /root/.pip/pip.conf
RUN mkdir -p /var/www/html/mysite
WORKDIR /var/www/html/mysite
ADD . /var/www/html/mysite
RUN chown -R www-data:www-data /var/www/html/mysite
# eee
RUN pip install -r requirements.txt
RUN sed -i 's/\r//' ./start.sh
USER www-data
RUN chmod +x ./start.sh
ENTRYPOINT ["./start.sh"]