FROM python:3.10.7-slim-buster

# setup environment variable
ENV DockerHOME=/app

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# copy requirements
COPY requirements.txt requirements.txt

# Install libpq-dev for psycopg2 python package
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# install all dependencies
RUN pip install -r requirements.txt

# copy whole project to your docker home directory.
COPY . $DockerHOME

# port where the Django app runs
EXPOSE 8000
# start server
CMD ["python", "/app/airline_erp/manage.py", "runserver"]

