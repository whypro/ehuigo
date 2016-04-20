# The FROM instruction sets the Base Image for subsequent instructions.
# Using Nginx as Base Image
FROM debian:wheezy

ENV EHUIGO_DIR /home/whypro/codes/ehuigo

RUN apt-get update
RUN apt-get -y install python python-pip python-dev libmysqlclient-dev nginx python-gevent gunicorn supervisor libjpeg-dev  libfreetype6-dev


RUN mkdir -p $EHUIGO_DIR
COPY . $EHUIGO_DIR
WORKDIR $EHUIGO_DIR
RUN pip install -r requirements.txt
COPY etc/supervisord.conf /etc/supervisord.conf
COPY etc/nginx.conf /etc/nginx/conf.d/ehuigo.conf
# RUN chmod 644 /etc/nginx/conf.d/ehuigo.conf
RUN /etc/init.d/nginx start

# RUN cd $EHUIGO_DIR

# USER ehuigo
EXPOSE 80


CMD supervisord -c /etc/supervisord.conf
# CMD ["python", "manage.py", "debug"]

#FROM nginx

# The RUN instruction will execute any commands
# Adding HelloWorld page into Nginx server
#RUN echo "Hello World DaoCloud!" > /usr/share/nginx/html/index.html

# The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime


# The CMD instruction provides default execution command for an container
# Start Nginx and keep it from running background
#CMD ["nginx", "-g", "daemon off;"]