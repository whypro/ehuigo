FROM debian:wheezy

ENV EHUIGO_DIR /home/whypro/codes/ehuigo

RUN apt-get update
RUN apt-get -y install python python-pip python-dev libmysqlclient-dev python-gevent gunicorn supervisor libjpeg-dev  libfreetype6-dev


RUN mkdir -p $EHUIGO_DIR
COPY . $EHUIGO_DIR
WORKDIR $EHUIGO_DIR
RUN pip install -r requirements.txt
COPY etc/supervisord.conf /etc/supervisord.conf
# COPY etc/nginx.conf /etc/nginx/conf.d/ehuigo.conf
# RUN chmod 644 /etc/nginx/conf.d/ehuigo.conf
# RUN /etc/init.d/nginx start

EXPOSE 80

CMD supervisord -c /etc/supervisord.conf
# CMD ["python", "manage.py", "debug"]
