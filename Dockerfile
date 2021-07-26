FROM microsoft/iis:latest

RUN apt-get update
RUN apt-get install python

RUN pip install Flask
RUN pip install sqlite3
RUN pip install SQLAlchemy

COPY . /opt/source-code

ENTRYPOINT FLASK_APP=/opt/source-code/app.py flask run

EXPOSE 80