# The FROM instruction sets the Base Image for subsequent instructions.
# Using Nginx as Base Image
FROM debian:wheezy

ENV EHUIGO_DIR $EHUIGO_DIR

RUN apt-get update
RUN apt-get -y install python python-pip python-dev libmysqlclient-dev nginx gunicorn

RUN useradd -m whypro
RUN chsh -s /bin/bash whypro
RUN usermod -G whypro,sudo whypro

#RUN pwd
USER whypro
RUN mkdir -p $EHUIGO_DIR
COPY . $EHUIGO_DIR
# WORKDIR $EHUIGO_DIR


#USER root
#RUN pwd
USER root
RUN pip install -r requirements.txt


ADD $EHUIGO_DIR/etc/supervisord.conf /etc/supervisord.conf
ADD $EHUIGO_DIR/etc/nginx/ehuigo.conf /etc/nginx/conf.d/ehuigo.conf
# RUN chmod 644 /etc/nginx/conf.d/ehuigo.conf

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