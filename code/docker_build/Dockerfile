FROM python:3
LABEL maintainer="rich@justcompile.it"

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
ENV AIRFLOW_HOME /usr/local/airflow

ENV LANGUAGE en_GB.UTF-8
ENV LANG en_GB.UTF-8
ENV LC_ALL en_GB.UTF-8
ENV LC_CTYPE en_GB.UTF-8
ENV LC_MESSAGES en_GB.UTF-8
ENV LC_ALL en_GB.UTF-8

# Airflow
ARG AIRFLOW_VERSION=1.9.0
ARG CELERY_VERSION=4.2.0
ARG AIRFLOW_HOME=/usr/local/airflow

RUN apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends locales \
    && sed -i 's/^# en_GB.UTF-8 UTF-8$/en_GB.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_GB.UTF-8 LC_ALL=en_GB.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow \
    && pip install Cython \
    && pip install pytz \
    && pip install apache-airflow[crypto,celery,postgres]==$AIRFLOW_VERSION \
    && pip install celery[redis]==$CELERY_VERSION \
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

RUN chown -R airflow: ${AIRFLOW_HOME}

USER airflow
WORKDIR ${AIRFLOW_HOME}

COPY . ${AIRFLOW_HOME}
# COPY ./dags ${AIRFLOW_HOME}

EXPOSE 8080 5555 8793

