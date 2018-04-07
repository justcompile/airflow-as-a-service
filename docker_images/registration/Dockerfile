# VERSION 1.8.2
# AUTHOR: Richard Hayes
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t justcompile/docker-airflow .
# SOURCE: https://github.com/justcompile/docker-airflow

FROM python:3.6-slim
MAINTAINER rich@justcompile.it

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

RUN pip install docker

COPY app.py /app.py

CMD python /app.py
