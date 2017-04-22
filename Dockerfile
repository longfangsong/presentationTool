FROM daocloud.io/python:3-onbuild
MAINTAINER longfangsong@icloud.com
EXPOSE 80
COPY . .
RUN apt-get update
RUN apt-get install nginx -y
COPY nginx.conf /etc/nginx/nginx.conf
RUN pip3 install -r requirements.txt
RUN python3 manage.py migrate --noinput
RUN python3 manage.py collectstatic --noinput
CMD nginx & gunicorn presentationTool.wsgi
