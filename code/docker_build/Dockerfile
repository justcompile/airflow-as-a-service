FROM python:3
LABEL maintainer="rich@justcompile.it"

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
ENV AIRFLOW_HOME /app/airflow
ENV LANGUAGE en_GB.UTF-8
ENV LANG en_GB.UTF-8
ENV LC_ALL en_GB.UTF-8
ENV LC_CTYPE en_GB.UTF-8
ENV LC_MESSAGES en_GB.UTF-8
ENV LC_ALL en_GB.UTF-8

WORKDIR /app/airflow

RUN apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends locales \
    && sed -i 's/^# en_GB.UTF-8 UTF-8$/en_GB.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_GB.UTF-8 LC_ALL=en_GB.UTF-8 \
    && useradd -ms /bin/bash -d $AIRFLOW_HOME airflow \
    && pip --no-cache-dir install apache-airflow \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /root/.cache/pip/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

USER airflow

ADD ./airflow.cfg airflow.cfg

EXPOSE 8080

